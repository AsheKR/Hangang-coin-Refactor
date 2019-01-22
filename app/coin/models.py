import re

import requests
from bs4 import BeautifulSoup
from django.db import models


class Coin(models.Model):
    CURRENCY_PAIR = []

    name = models.CharField(
        max_length=20,
        unique=True,
    )

    @classmethod
    def get_or_create_coin_with_currency_pair(cls, currency):
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
