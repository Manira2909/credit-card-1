from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from.models import CreditCard, Transaction
from.utils import encrypt_card, luhn_check
from django.db.models import Sum, Count
from django.utils import timezone
import uuid, re

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_card(request):
    number = request.data.get('card_number', '').replace(" ", "")
    cvv = request.data.get('cvv', '')
    holder = request.data.get('holder_name', '')
    expiry = request.data.get('expiry_date', '') # 12/28

    # 1. CVV check only - NO STORE
    if not re.match(r'^\d{3,4}$', cvv):
        return Response({"error": "Invalid CVV"}, status=400)

    # 2. Luhn check
    if not luhn_check(number):
        return Response({"error": "Invalid Card Number"}, status=400)

    # 3. Expiry parse
    try:
        month, year = expiry.split('/')
        month = int(month); year = int("20"+year) if len(year)==2 else int(year)
    except:
        return Response({"error": "Invalid Expiry format MM/YY"}, status=400)

    # 4. Encrypt
    encrypted = encrypt_card(number)

    card = CreditCard.objects.create(
        user=request.user,
        holder_name=holder,
        encrypted_number=encrypted,
        last4=number[-4:],
        expiry_month=month,
        expiry_year=year
    )
    return Response({"message": "Card added", "card": f"****{card.last4}"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_cards(request):
    cards = CreditCard.objects.filter(user=request.user, is_active=True)
    data = [{"id": c.id, "holder": c.holder_name, "last4": c.last4, "expiry": f"{c.expiry_month}/{str(c.expiry_year)[-2:]}"} for c in cards]
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pay(request):
    card_id = request.data.get('card_id')
    amount = request.data.get('amount')
    try:
        card = CreditCard.objects.get(id=card_id, user=request.user, is_active=True)
    except CreditCard.DoesNotExist:
        return Response({"error": "Card not found"}, status=404)

    txn = Transaction.objects.create(
        user=request.user,
        card=card,
        amount=amount,
        ref_id=f"TXN-{uuid.uuid4().hex[:8].upper()}"
    )
    return Response({"message": "Payment Success", "ref_id": txn.ref_id})

# NEW - Dashboard Summary API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    user = request.user

    # 1. Aggregations - OPTIMIZED. DB la ye sum/count pannidum
    total_txns = Transaction.objects.filter(user=user).count()

    total_spent = Transaction.objects.filter(user=user, status='success').aggregate(
        total=Sum('amount')
    )['total'] or 0

    # Current month
    now = timezone.now()
    current_month_spent = Transaction.objects.filter(
        user=user,
        status='success',
        created_at__year=now.year,
        created_at__month=now.month
    ).aggregate(total=Sum('amount'))['total'] or 0

    # 2. Available Credit - User model la balance field irukanum
    available_credit = float(user.balance) - float(total_spent)

    # 3. Last 5 Transactions with JOIN
    last_5_qs = Transaction.objects.filter(user=user).select_related('card').order_by('-created_at')[:5]

    last_5 = [
        {
            "amount": float(t.amount),
            "masked_card_number": f"**** **** {t.card.last4}",
            "date": t.created_at,
            "status": t.status
        } for t in last_5_qs
    ]

    return Response({
        "total_transactions": total_txns,
        "total_amount_spent": float(total_spent),
        "current_month_spending": float(current_month_spent),
        "available_credit_limit": available_credit,
        "last_5_transactions": last_5
    })