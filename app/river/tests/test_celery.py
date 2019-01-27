from river.tasks import get_river_temperature_with_celery


class TestRiverCeleryTask:

    def test_get_river_temperature(self):
        task = get_river_temperature_with_celery.apply_async()
        assert task.status == 'SUCCESS', 'get_all_coin_method_with_celery Failed'
