from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class FunctionalTest(LiveServerTestCase):

    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)

    def tearDown(self):
        self.browser.quit()
