from coin.tasks import get_all_coin_with_celery


class TestCoinCeleryTask:

    def test_get_all_coin_method_return_status_is_success(self):
        task = get_all_coin_with_celery.apply_async()
        assert task.status == 'SUCCESS', 'get_all_coin_method_with_celery Failed'
