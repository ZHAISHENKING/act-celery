from flask_celery import Celery
from flask_redis import Redis

celery = Celery()
redis = Redis()