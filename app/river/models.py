import os
import time

from bs4 import BeautifulSoup
from django.conf import settings
from django.db import models
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


class River(models.Model):
    temperature = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_river_temperature(cls):
        url = 'http://www.koreawqi.go.kr/index_web.jsp'

        browser = webdriver.PhantomJS(os.path.join(settings.ROOT_DIR, '.bin', 'phantomjs'))
        browser.get(url)

        start_time = time.time()
        max_wait = 10
        temperature = None

        while True:
            try:
                browser.switch_to.frame('MainFrame')
                browser.find_element_by_id('container').find_element_by_id('state')
                browser.find_element_by_class_name('tab_container').find_element_by_class_name('timetable')
                td = browser.find_element_by_xpath('//*[@id="div_layer_btn1_r1"]/table/tbody/tr[18]').get_attribute(
                    'outerHTML')
                browser.switch_to.default_content()

                soup = BeautifulSoup(td, 'html.parser')
                td_list = soup.select('td')

                temperature = td_list[0].get_text(strip=True)
                if not temperature:
                    raise ValueError
                else:
                    break
            except (AssertionError, WebDriverException, ValueError) as e:
                if time.time() - start_time > max_wait:
                    raise e
            finally:
                browser.quit()

        River.objects.create(
            temperature=temperature,
        )
