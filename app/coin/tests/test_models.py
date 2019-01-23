import pytest

from coin.models import Coin, CoinValue


class TestCoinModel:

    def create_coinvalue_stub(self):
        coin = Coin.get_or_create_coin_using_currency_pair('Bitcoin')
        coin_value = CoinValue.create_now_coinvalue_with_coin(coin)

        assert CoinValue.objects.last() == coin_value, 'Save CoinValue Failed'

        return coin_value

    def test_create_coin_that_korbit_supports(self):
        Coin.get_top_10_coins_that_korbit_supports()

        assert len(Coin.CURRENCY_PAIR) != 0, 'Crawling Currency Failed'

        for currency, _ in Coin.CURRENCY_PAIR:
            coin = Coin.get_or_create_coin_using_currency_pair(currency)
            assert Coin.objects.get(name=currency) == coin, 'Save Currency Failed'

    def test_create_coinvalue_using_coin(self):
        self.create_coinvalue_stub()

    def test_create_coinvalue_if_first_value_of_the_day_attribute_is_day_master_true(self):
        first_value = self.create_coinvalue_stub()
        second_value = self.create_coinvalue_stub()

        assert first_value.is_day_master is True, 'is_day_master setting Failed'
        assert second_value.is_day_master is False, 'is_day_master setting Failed'

    def test_crawling_all_coin(self):
        Coin.get_all_coins_with_coin_Value()

        assert Coin.objects.count() == 10, 'Ten Coin Data Crawling Failed'
        assert CoinValue.objects.filter(is_day_master=True).count() == 10, 'Ten CoinValue Crawling Failed'