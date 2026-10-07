from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import UserProfile, Card, Transaction

@csrf_exempt
#@login_required
def pay(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            card_last4 = data.get('card_last4')
            amount = float(data.get('amount', 0))

            # 1. UserProfile iruka nu check pannu. Illana create pannu
            profile, created = UserProfile.objects.get_or_create(
                user=request.user,
                defaults={'balance': 50000} # pudhu user na 50000 balance
            )

            # 2. Balance check
            if profile.balance < amount:
                return JsonResponse({'error': 'Insufficient balance'}, status=400)

            # 3. Balance la irundhu minus pannu
            profile.balance -= amount
            profile.save()

            # 4. Transaction history la add pannu
            Transaction.objects.create(
                user=request.user,
                card_last4=card_last4,
                amount=amount
            )

            return JsonResponse({
                'message': 'Payment Successful',
                'new_balance': profile.balance
            }, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
@login_required
def add_card(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        card_number = data.get('card_number')
        Card.objects.create(user=request.user, card_number=card_number)
        return JsonResponse({'message': 'Card added'})
    return JsonResponse({'error': 'Invalid method'}, status=405)


@login_required
def dashboard_summary(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user, defaults={'balance': 50000})
    cards = Card.objects.filter(user=request.user).count()
    return JsonResponse({
        'balance': profile.balance,
        'cards': cards
    })


@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')
    data = [
        {
            'card_last4': t.card_last4,
            'amount': t.amount,
            'timestamp': t.timestamp
        } for t in transactions
    ]
    return JsonResponse({'transactions': data})