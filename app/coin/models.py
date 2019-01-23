import re
from datetime import datetime, timedelta, time

import requests
from bs4 import BeautifulSoup
from django.db import models
from django.utils.timezone import make_aware


class Coin(models.Model):
    CURRENCY_PAIR = []

    name = models.CharField(
        max_length=20,
        unique=True,
    )

    def __str__(self):
        return self.name

    @classmethod
    def get_or_create_coin_using_currency_pair(cls, currency):
        coin, _ = Coin.objects.get_or_create(name=currency)
        return coin

    @classmethod
    def get_top_10_coins_that_korbit_supports(cls):
        """
        korbit에서 지원하는 상위 10개의 코인을 가져와 Choices 형태로 저장

        CURRENCY_PAIR ('CURRENCY', 'PAIR')
        """
        if not cls.CURRENCY_PAIR:
            url = 'https://coinmarketcap.com/exchanges/korbit/'
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            trs = soup.select_one('table').find_all('tr')[1:]
            for i, tr in enumerate(trs):
                if i == 10:
                    return
                currency = tr.select_one('.link-secondary').text
                pair = tr.find('a', href=re.compile(r'https://www.korbit.co.kr/*')).text
                pair_name = re.sub(r'(\w+)/(\w+)', r'\g<1>_\g<2>', pair.lower())
                cls.CURRENCY_PAIR.append((currency, pair_name))

    @classmethod
    def get_all_coins_with_coin_value(cls):
        if not cls.CURRENCY_PAIR:
            cls.get_top_10_coins_that_korbit_supports()

        for currency, pair in cls.CURRENCY_PAIR:
            coin = cls.get_or_create_coin_using_currency_pair(currency)
            CoinValue.create_now_coinvalue_with_coin(coin)


    @property
    def today_master_value(self):
        return self.coinvalue_set.filter(is_day_master=True).last().value

    @property
    def latest_value(self):
        return self.coinvalue_set.last().value


class CoinValue(models.Model):
    coin = models.ForeignKey(
        Coin,
        on_delete=models.CASCADE,
    )
    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, )
    is_day_master = models.BooleanField(default=False, )

    def __str__(self):
        return self.coin.name + '의 현재값: ' + str(self.value)

    @classmethod
    def create_now_coinvalue_with_coin(cls, coin):

        def get_current_coin_value_through_korbit_api(pair):
            def message(data):
                """
                json 파일을 받아 다음과 같이 사용하면 아래 내용을 가져올 수 있다.
                """
                last_price = int(data.get('last'))
                high_price = int(data.get('high'))
                low_price = int(data.get('low'))
                bid_price = int(data.get('bid'))
                ask_price = int(data.get('ask'))
                timestamp = datetime.fromtimestamp(int(data.get('timestamp') / 1000))

                # for Debug
                return '''
                    현재가: {:,}
                    최근 24시간 최고가: {:,}
                    최근 24시간 최저가: {:,}
                    매수 호가: {:,}
                    매도 호가: {:,}
                    최종 체결 시각: {}
                    '''.format(last_price, high_price, low_price, bid_price, ask_price, timestamp)

            base_url = 'https://api.korbit.co.kr/v1/ticker/detailed'
            url = '{}?currency_pair={}'.format(base_url, pair)
            response = requests.get(url)
            return response.json()

        json_data = get_current_coin_value_through_korbit_api(dict(coin.CURRENCY_PAIR)[coin.name])
        value = int(float(json_data.get('last')))
        coin_value = CoinValue(
            coin=coin,
            value=value,
        )

        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = make_aware(datetime.combine(today, time()))
        today_end = make_aware(datetime.combine(tomorrow, time()))

        if not CoinValue.objects.filter(coin=coin, created_at__lte=today_end, created_at__gte=today_start):
            coin_value.is_day_master = True

        coin_value.save()

        return coin_value
