from django.contrib import admin
from .models import CreditCard, Transaction, Address

admin.site.register(CreditCard)
admin.site.register(Transaction)
admin.site.register(Address)