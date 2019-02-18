import logging

from celery import Celery
from celery.signals import setup_logging
from django.conf import settings
from raven import Client
from raven.contrib.celery import register_logger_signal, register_signal

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

client = Client('https://925b7abfc0b74ef9bc6d3175516974a9:7aab90be714a49498161f704bd0df8de@sentry.io/1372674')

# register a custom filter to filter out duplicate logs
register_logger_signal(client)

# The register_logger_signal function can also take an optional argument
# `loglevel` which is the level used for the handler created.
# Defaults to `logging.ERROR`
register_logger_signal(client, loglevel=logging.INFO)

# hook into the Celery error handler
register_signal(client)

# The register_signal function can also take an optional argument
# `ignore_expected` which causes exception classes specified in Task.throws
# to be ignored
register_signal(client, ignore_expected=True)


app.autodiscover_tasks()
