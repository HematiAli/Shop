from celery import Celery
from datetime import timedelta
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'A.settings')

celery_app = Celery('A') #name of django project
celery_app.autodiscover_tasks()#by default find=> task.py, if I change use realted_name='slkfasl.py'
celery_app.conf.broker_url = "amqp://" #addres rabbitmq on local host
celery_app.conf.result_backend = 'rpc://'
celery_app.conf.task_serializer = 'json'
celery_app.conf.result_serializer = 'pickle'
celery_app.conf.accept_content = ['json', 'pickle']
celery_app.conf.result_expires = timedelta(days=1)
celery_app.conf.worker_prefetch_multiplier = 1
celery_app.conf.task_always_eager = False # when you do task don't block user

# add to __init__.py
