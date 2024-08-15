from django.db import models
from django.contrib.auth.models import AbstractUser
from functools import cached_property


COUNTRY_CHOICES = [
    ("ru", "Russia"),
    ("us", "USA"),
    ("en", "England"),
    ("fr", "France")
]

STATUS_CHOICES = [
    ('Active', 'Active'),
    ('Inactive', 'Inactive')
]

TRANSACTION_STATUS_CHOICES = [
    ('Completed', 'Completed'),
    ('Pending', 'Pending'),
    ('Canceled', 'Canceled')
]


class Token(models.Model):
    short_name = models.CharField(max_length=16, default="")
    long_name = models.CharField(max_length=128, default="")
    value = models.DecimalField(max_digits=8, decimal_places=2)
    check_date = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.short_name


class TokenInWallet(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE, related_name="token_in_wallet")
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    wallet = models.ForeignKey('Wallet', related_name="tokens", on_delete=models.CASCADE, null=True)

    @cached_property
    def total_token_value(self):
        return self.token.value * self.amount

    def save(self, *args, **kwargs):
        super(TokenInWallet, self).save(*args, **kwargs)
        self.wallet.balance += self.total_token_value
        self.wallet.save()

    # def __str__(self):
    #     return self.wallet
    

class Wallet(models.Model):

    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
        
    def __str__(self):
        return f"{self.user}'s wallet"
    

class User(AbstractUser):
    
    email = models.EmailField(blank=True, unique=True)
    image = models.ImageField(upload_to='static/profiles', blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="Active")
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.username
    

class Transaction(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="outcoming_transactions")
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="incoming_transactions")
    date = models.DateTimeField(auto_now_add=True, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=10, default=0)
    status = models.CharField(choices=TRANSACTION_STATUS_CHOICES, max_length=9, default="Pending")
    token = models.CharField(max_length=5, default="")

    def __str__(self):
        return f"Transaction from {self.user_from} to {self.user_to} with {self.token}"
    

class TokenHistory(Token):
    pass
