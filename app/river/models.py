import requests
from bs4 import BeautifulSoup
from django.db import models


class River(models.Model):
    temperature = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_river_temperature(cls):
        url = 'https://www.wpws.kr/hangang/'

        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'html.parser')

        temp = soup.select_one('p#temp').text[:3]

        River.objects.create(
            temperature=temp,
        )
