import os

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from coin.models import Coin
from river.models import River


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.PhantomJS(os.path.join(settings.ROOT_DIR, '.bin', 'phantomjs'))
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
