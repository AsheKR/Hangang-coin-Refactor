import pytest

from .base import FunctionalTest


class PageConversionTest(FunctionalTest):

    def test_checkout_other_coin(self):
        # 홈페이지를 방문한다.
        self.browser.get(self.live_server_url)

        # 코인 선택창을 연다.
        elem = self.browser.find_element_by_id('select-coin-button')
        elem.click()

        # 코인을 선택한다.
        elem = self.browser.find_elements_by_css_selector("input[type='radio']")[5]
        before_checked_coin_name = elem.get_attribute('value')
        elem.click()

        # 확인 버튼을 누른다.
        self.browser.find_element_by_id('send_coin_name').click()

        # URL에서 페이지 이동을 확인한다.
        self.assertIn(before_checked_coin_name, self.browser.current_url)

        # 화면에 내려온 데이터의 코인 이름과 값을 확인한다.
        coin_name = self.browser.find_element_by_id('coin_name').text
        self.assertIn(before_checked_coin_name, coin_name)

        # 체크되어있는 코인이 현재 코인인지 확인한다.
        after_checked_coin_name = self.browser.find_element_by_css_selector("input[type='radio']:checked").get_attribute('value')
        self.assertIn(after_checked_coin_name, coin_name)
