import time

from bs4 import BeautifulSoup
from django.db import models
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options


class River(models.Model):
    temperature = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_river_temperature(cls):
        url = 'http://www.koreawqi.go.kr/index_web.jsp'

        display = Display(visible=0, size=(1366, 768))
        display.start()

        options = Options()
        options.headless = True
        browser = webdriver.Firefox(options=options)

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
                display.stop()

        River.objects.create(
            temperature=temperature,
        )
