import pytest
from django.contrib.staticfiles import finders

from .base import FunctionalTest


class PageConversionTest(FunctionalTest):

    @pytest.mark.smoke
    def test_checkout_other_coin(self):
        # 홈페이지를 방문한다.
        self.browser.get(self.live_server_url)

        # 코인을 선택한다.
        elem = self.browser.find_elements_by_css_selector("input[type='radio']")[5]
        coin_name_from_checked = elem.get_attribute('value')
        elem.click()

        # 확인 버튼을 누른다.
        self.browser.find_element_by_id('send_coin_name').click()

        # URL에서 페이지 이동을 확인한다.
        self.assertIn(self.browser.current_url, coin_name_from_checked)

        # 화면에 내려온 데이터의 코인 이름과 값을 확인한다.
        coin_name = self.browser.find_element_by_id('coin_name').text
        self.assertEqual(coin_name_from_checked, coin_name)
