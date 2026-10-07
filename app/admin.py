from django.contrib import admin
from .models import UserProfile, Card, Transaction # CreditCard illa

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_number')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_last4', 'amount', 'timestamp')
    list_filter = ('timestamp',)