from django.contrib import admin
from .models import (
    Token, 
    User, 
    Transaction,
    Wallet,
    TokenInWallet
)


admin.site.register(Token)
admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(Wallet)
admin.site.register(TokenInWallet)