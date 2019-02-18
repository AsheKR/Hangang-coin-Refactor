from celery.utils.log import get_task_logger

from coin.models import Coin
from config.celery import app


@app.task
def get_all_coin_with_celery():
    logger = get_task_logger(__name__)

    try:
        Coin.get_all_coins_with_coin_value()
    except Exception as e:
        logger.error(e)
