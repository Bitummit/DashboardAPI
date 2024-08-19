from django.contrib import admin
from .models import (
    Token, 
    User, 
    Transaction,
    Wallet,
    TokenInWallet,
    TokenHistory
)


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    readonly_fields =  ('check_date',) 


@admin.register(TokenHistory)
class TokenHistoryAdmin(admin.ModelAdmin):
    readonly_fields =  ('check_date',)


admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(Wallet)
admin.site.register(TokenInWallet)

