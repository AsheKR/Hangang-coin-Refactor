from coin.models import Coin


class TestCoinModel:

    def test_create_coin_that_korbit_supports(self):
        currency_list = Coin.get_top_10_coins_that_korbit_supports()

        for currency, _ in currency_list:
            coin = Coin.get_or_create_coin_with_curreny_pair(currency)
            assert Coin.objects.get(name=currency) == coin
