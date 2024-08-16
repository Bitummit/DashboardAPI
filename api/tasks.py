from django.db import transaction
import requests

from DashboardAPI.celery import app
from DashboardAPI.settings import NINJAS_API_KEY
from .models import Token
from celery import shared_task

NINJAS_API_URL = 'https://api.api-ninjas.com/v1'


def get_token_price(token_to_search, token_short_name):
    token_info = requests.get(f"{NINJAS_API_URL}/cryptoprice?symbol={token_to_search}", headers={'X-Api-Key': NINJAS_API_KEY}).json()
    token = Token.objects.get(short_name=token_short_name)
    print(NINJAS_API_KEY)
    print(token_info)
    token.value = token_info['price']
    token.save()

@app.task
def get_token_values():
    get_token_price("BTCUSDT", "BTC")
    get_token_price("ETHUSDT", "ETH")
    get_token_price("SOLUSDT", "SOL")
    get_token_price("LTCUSDT", "LTC")


# @app.task    don't work!!!
# def make_transaction(token_user_from, user_to, amount, token, new_transaction):
#     with transaction.atomic():
#         print(token_user_from)
#         token_user_from.amount -= amount
#         print(2)
#         token_user_from.save()
#         token_user_to, created = user_to.wallet.tokens.select_related("token", "wallet").get_or_create(token=token, wallet=user_to.wallet)
#         print(3)
#         token_user_to.amount += amount
#         token_user_to.save()
#         print(4)
#         new_transaction.status = "Completed"
#         new_transaction.save()
#         return new_transaction