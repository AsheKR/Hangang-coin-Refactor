from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from coin.models import Coin
from river.models import River


class FunctionalTest(LiveServerTestCase):

    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)
        self.create_coinvalue_stub()
        self.create_river_stub()

    def tearDown(self):
        self.browser.quit()

    def create_coinvalue_stub(self):
        Coin.get_all_coins_with_coin_value()
        self.coin = Coin.objects.first()

    def create_river_stub(self):
        River.get_river_temperature()
        self.river = River.objects.first()