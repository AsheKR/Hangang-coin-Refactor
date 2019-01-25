import pytest

from coin.models import Coin, CoinValue
from river.models import River


class TestCoinView:

    def create_stub_coinvalue(self, second_value, coin_name):
        coin, _ = Coin.objects.get_or_create(name=coin_name)
        CoinValue.objects.create(coin=coin, value=100, is_day_master=True)
        CoinValue.objects.create(coin=coin, value=second_value)

        return coin

    def test_home_page_returns_correct_html(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_index_have_current_coin_value_and_is_day_master_coin_value_and_coin_name(self, client):
        coin = self.create_stub_coinvalue(200, 'Bitcoin')

        response = client.get('/')

        html = response.content.decode('utf8')
        assert coin.name in html, 'CoinName Not Included'
        assert str(coin.coinvalue_set.first().value) in html, 'First CoinValue Not Included'
        assert str(coin.coinvalue_set.last().value) in html, 'Last CoinName Not Included'

    def test_return_wait_page_if_there_is_no_coin_value_data(self, client):
        response = client.get('/')

        html = response.content.decode('utf8')
        assert '준비중입니다.' in html, 'Not have Coin, Error Page not returned'

    def test_return_wait_page_when_latest_coin_value_is_smaller_than_master_coin_value_and_not_have_river_data(self, client):
        coin = self.create_stub_coinvalue(50, 'Bitcoin')

        assert coin.latest_value < coin.today_master_value, 'master_value must be big'

        response = client.get('/')
        html = response.content.decode('utf8')
        assert '준비중입니다.' in html, 'Error Page must be returned'

    def test_return_correct_page_with_river_data_when_latest_coin_value_is_smaller_than_master_coin_value(self, client):
        coin = self.create_stub_coinvalue(50, 'Bitcoin')
        river = River.objects.create(temperature=2.4)

        assert coin.latest_value < coin.today_master_value, 'master_value must be big'

        response = client.get('/')
        html = response.content.decode('utf8')
        assert str(river.temperature) in html, 'River Data not Included'

    def test_return_correct_page_with_coin_list(self, client):
        Coin.get_all_coins_with_coin_value()

        response = client.get('/')
        html = response.content.decode('utf8')
        for currency, _ in Coin.CURRENCY_PAIR:
            assert currency in html, 'CURRENCY_PAIR not Included'

    def test_return_specific_coin_page(self, client):
        coin_first = self.create_stub_coinvalue(200, 'Bitcoin')
        coin_second = self.create_stub_coinvalue(200, 'NewCoin')

        response = client.get('/coin/'+coin_second.name+'/')
        html = response.content.decode('utf8')
        assert coin_second.name in html, 'specific coin name not appear'
