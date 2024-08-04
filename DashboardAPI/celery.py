import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DashboardAPI.settings")

app = Celery("DashboardAPI")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()