from captcha import Captcha
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager


class Browser():
    def __init__(self, config):
        self.config  = config
        self.service = Service(GeckoDriverManager().install())
        self.driver  = webdriver.Firefox(service = self.service)

    def write_html(self, content):
        with open('source.html', 'w') as file:
            file.write(content)

    def get(self, write=False):
        self.driver.get(self.config['url']['trb'])

        input_name = self.driver.find_element("name", self.config['fields']['num'])
        self.driver.execute_script('arguments[0].value="Blorblespack"', input_name)
        input_code = self.driver.find_element("name", self.config['fields']['pas'])
        self.driver.execute_script('arguments[0].value="Smorkleplack"', input_code)
        input_name.submit()

        if write == True:
            self.write_html(self.driver.page_source)
            print("HTML file written")
        
        # self.driver.close()
