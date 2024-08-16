from django.db import transaction

from DashboardAPI.celery import app
from DashboardAPI.settings import NINJAS_API_KEY
from .models import Token
from celery import shared_task



@app.task
def get_token_values():
    token = Token.objects.create(short_name="Test", long_name="Long test name", value=3422)
    token.save()


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