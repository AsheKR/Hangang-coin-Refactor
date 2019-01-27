import pytest
from selenium.common.exceptions import NoSuchElementException

from coin.models import Coin
from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_visit_our_site(self):
        # 홈페이지를 방문한다.
        self.browser.get(self.live_server_url)

        # 홈페이지의 타이틀이 한강 코인인것을 확인한다.
        self.assertIn('한강 코인', self.browser.title)

        # 현재 코인값과 대표값이 내려왔는지 확인한다.
        coin_name = self.browser.find_element_by_id('coin_name').text
        today_master_value = self.browser.find_element_by_id('today_master_value').text
        latest_value = self.browser.find_element_by_id('latest_value').text

        self.assertIn(self.coin.name, coin_name)
        self.assertIn(str(self.coin.today_master_value), today_master_value)
        self.assertIn(str(self.coin.latest_value), latest_value)

    def test_river_temperature_appears_in_a_particular_situation(self):
        # today_master_value보다 latest_value가 떨어졌다면 한강 수온을 가져온다.
        self.coin.coinvalue_set.create(value=self.coin.latest_value - 100)
        self.browser.get(self.live_server_url)

        # 한강수온이 있는지 확인한다.
        river_temperature = self.browser.find_element_by_id('river_temperature').text
        self.assertIn(str(self.river.temperature), river_temperature)

        # today_master_value보다 latest_value가 올라갔다면 한강 수온을 가져오지 않는다.
        self.coin.coinvalue_set.create(value=self.coin.latest_value + 100)
        self.browser.get(self.live_server_url)

        # 한강수온이 있는지 확인한다.
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('river_temperature')

    def test_ten_coin_list_appears_in_index(self):
        self.browser.get(self.live_server_url)

        coin_list = Coin.CURRENCY_PAIR

        select_coin_list = self.browser.find_element_by_id('select_coin').get_attribute('innerHTML')
        print(select_coin_list)

        for currency, _ in coin_list:
            self.assertIn(currency, select_coin_list)

        coin = Coin.objects.first()

        elem = self.browser.find_element_by_css_selector("input[type='radio'][value='"+coin.name+"']")
        self.assertEqual(elem.is_selected(), True)
