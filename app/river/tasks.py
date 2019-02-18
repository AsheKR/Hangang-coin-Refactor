from celery.utils.log import get_task_logger

from config.celery import app
from river.models import River


@app.task
def get_river_temperature_with_celery():
    logger = get_task_logger(__name__)

    try:
        River.get_river_temperature()
    except Exception as e:
        logger.error(e)
