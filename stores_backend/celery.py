import os
from celery import Celery
# from api.helpers import send_email as send_email_helper
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stores_backend.settings.dev')

app = Celery('stores_backend', broker='pyamqp://signscloud:generacion2022@rabbitmq//')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()