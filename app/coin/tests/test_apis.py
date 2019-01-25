import json

from coin.models import Coin, CoinValue


class TestCoinApi:

    def create_stub_coinvalue(self, second_value, coin_name):
        coin, _ = Coin.objects.get_or_create(name=coin_name)
        CoinValue.objects.create(coin=coin, value=100, is_day_master=True)
        CoinValue.objects.create(coin=coin, value=second_value)

        return coin

    def test_retrieve_coin_api(self, client):
        coin = self.create_stub_coinvalue(200, 'FakeCoin')

        json_data = json.loads(client.get('/api/coin/'+coin.name+'/').content.decode('utf8'))

        assert json_data['latest_value'] == coin.latest_value
        assert json_data['today_master_value'] == coin.today_master_value
        assert json_data['percent'] == 100.0
        assert json_data['coin_name'] == coin.name
        assert 'p_15_20' in json_data['image']
