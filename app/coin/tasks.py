from coin.models import Coin
from config.celery import app


@app.task
def get_all_coin_with_celery():
    Coin.get_all_coins_with_coin_value()