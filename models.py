from django.db import models
from django.contrib.auth.models import User

class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    holder_name = models.CharField(max_length=100)
    last4 = models.CharField(max_length=4)
    expiry_month = models.IntegerField()
    expiry_year = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.holder_name} - ****{self.last4}"

class Transaction(models.Model):
    credit_card = models.ForeignKey(CreditCard, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    merchant = models.CharField(max_length=100, default="Test Merchant")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.credit_card} - {self.amount}"

# PUDHUSA ADDRESS MA!
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.street}, {self.city} - {self.pincode}"