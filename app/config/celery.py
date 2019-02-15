from celery import Celery
from celery.signals import setup_logging
from django.conf import settings


if settings.DEBUG is True:
    url = 'localhost'
else:
    url = 'coin-redis.ke2lqx.0001.apn2.cache.amazonaws.com'

app = Celery('tasks',
             broker='redis://'+url+':6379/0',
             )

app.conf.update(
    CELERY_TIMEZONE='Asia/Seoul',
    CELERYBEAT_SCHEDULE={
        'crawling-coin-every-1-min': {
            'task': 'coin.tasks.get_all_coin_with_celery',
            'schedule': 60.0,
            'args': (),
        },
        'crawling-river-every-one-day': {
            'task': 'river.tasks.get_river_temperature_with_celery',
            'schedule': 86400.0,
            'args': (),
        },
    }
)


app.autodiscover_tasks()
