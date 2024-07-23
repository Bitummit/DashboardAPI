from django.db import models
from django.contrib.auth.models import AbstractUser


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

    @property
    def total_token_value(self):
        return self.token.value * self.amount


class Wallet(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name="wallet")

    @property
    def balance(self):
        total = 0
        for token in self.tokens.all():
            total += token.total_token_value
        total = "%.2f" % total
        # total += token.total_token_value for token in self.tokens.all()
        return total 

    def __str__(self):
        return f"{self.user}'s wallet"
    


class User(AbstractUser):
    
    email = models.EmailField(blank=True, unique=True)
    image = models.ImageField(upload_to='static/profiles', blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)


class Transaction(models.Model):
    pass
''' from to date amount token'''
