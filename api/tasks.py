from DashboardAPI.celery import app
from DashboardAPI.settings import NINJAS_API_KEY
from .models import Token

@app.task
def get_token_values():
    token = Token.objects.create(short_name="Test", long_name="Long test name", value=3422)
    token.save()