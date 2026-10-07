from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=50000)

    def __str__(self):
        return f"{self.user.username} - Balance: {self.balance}"


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16) # 16 digit mattum
    
    def __str__(self):
        return f"{self.user.username} - ****{self.card_number[-4:]}"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_last4 = models.CharField(max_length=4)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - ₹{self.amount}"