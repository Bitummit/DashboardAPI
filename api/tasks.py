from django.db import transaction
import requests
from django.forms.models import model_to_dict
import datetime

from DashboardAPI.celery import app
from DashboardAPI.settings import FIRST_PART_NINJAS_API_KEY, SECOND_PART_NINJAS_API_KEY
from .models import Token, TokenHistory
from celery import shared_task

NINJAS_API_URL = 'https://api.api-ninjas.com/v1'


def get_token_price(token_to_search, token_short_name):
    token_info = requests.get(f"{NINJAS_API_URL}/cryptoprice?symbol={token_to_search}", headers={'X-Api-Key': FIRST_PART_NINJAS_API_KEY + "==" + SECOND_PART_NINJAS_API_KEY}).json()
    token = Token.objects.get(short_name=token_short_name)
    token_dict = model_to_dict(token)
    token_dict.pop("id")
    TokenHistory.objects.create(**token_dict)
    token.value = token_info['price']
    token.check_date = datetime.datetime.now()
    token.save()


@app.task
def get_token_values():
    get_token_price("BTCUSDT", "BTC")
    get_token_price("ETHUSDT", "ETH")
    get_token_price("SOLUSDT", "SOL")
    get_token_price("LTCUSDT", "LTC")


# @app.task    doesn't work!!!
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