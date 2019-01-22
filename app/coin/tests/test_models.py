import pytest

from coin.models import Coin


class TestCoinModel:

    def test_create_coin_that_korbit_supports(self):
        Coin.get_top_10_coins_that_korbit_supports()

        assert len(Coin.CURRENCY_PAIR) != 0, 'Crawling Currency Failed'

        for currency, _ in Coin.CURRENCY_PAIR:
            coin = Coin.get_or_create_coin_with_currency_pair(currency)
            assert Coin.objects.get(name=currency) == coin, 'Save Currency Failed'
