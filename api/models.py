from django.db import models
from django.contrib.auth.models import AbstractUser


COUNTRY_CHOICES = [
        ("ru", "Russia"),
        ("us", "USA"),
        ("en", "England"),
        ("fr", "France")
    ]


class Token(models.Model):
    name = models.CharField(max_length=128)
    value = models.IntegerField()
    check_date = models.DateField()


class Wallet(models.Model):
    tokens = models.ManyToManyField(Token, related_name="wallet")
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name="wallet")

    def total_balance(self):
        total = 0

        for token in self.tokens:
            total += token.value

        return total


class User(AbstractUser):
    
    image = models.ImageField(upload_to='static/profiles')
    phone = models.CharField(max_length=12)
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)


class Transaction(models.Model):
    pass
''' from to date amount token'''
