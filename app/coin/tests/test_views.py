import pytest

from coin.models import Coin, CoinValue


class TestCoinView:

    def create_stub_coinvalue(self, second_value):
        coin = Coin.objects.create(name='Bitcoin')
        CoinValue.objects.create(coin=coin, value=100, is_day_master=True)
        CoinValue.objects.create(coin=coin, value=second_value)

        return coin

    def test_home_page_returns_correct_html(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_index_have_current_coin_value_and_is_day_master_coin_value_and_coin_name(self, client):
        coin = self.create_stub_coinvalue(200)

        response = client.get('/')

        html = response.content.decode('utf8')
        assert coin.name in html, 'CoinName Not Included'
        assert str(coin.coinvalue_set.first().value) in html, 'First CoinValue Not Included'
        assert str(coin.coinvalue_set.last().value) in html, 'Last CoinName Not Included'

    def test_do_not_have_coin_data_return_wait_page(self, client):
        response = client.get('/')

        html = response.content.decode('utf8')
        assert '준비중입니다.' in html, 'Not have Coin, Error Page not returned'

    def test_do_not_have_two_coin_value_data_return_wait_page(self, client):
        Coin.objects.create(name='stub')
        response = client.get('/')

        html = response.content.decode('utf8')
        assert '준비중입니다.' in html, 'Not have two CoinValue, Error Page not returned'
