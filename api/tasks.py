from celery import shared_task
from DashboardAPI.settings import NINJAS_API_KEY


@shared_task
def get_token_values():
    pass