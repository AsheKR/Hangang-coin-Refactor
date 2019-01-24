from config.celery import app
from river.models import River


@app.task
def get_river_temperature_with_celery():
    River.get_river_temperature()