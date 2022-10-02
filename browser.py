import sys
from captcha import Captcha
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager


class Browser():
    def __init__(self, config, destination):
        self.config  = config
        match destination:
            case 'trb':
                url = self.config['url']['trb']
            case 'ist':
                url = self.config['url']['ist']
            case _:
                print('Invalid URL. Available options: [trb, ist]')
                sys.exit()
        self.service = Service(GeckoDriverManager().install())
        self.driver  = webdriver.Firefox(service = self.service)
        self.driver.get(url)

    def write_html(self):
        with open('source.html', 'w') as file:
            file.write(self.driver.page_source)
        self.driver.close()

    def automate(self):
        input_name = self.driver.find_element("name", self.config['fields']['num'])
        self.driver.execute_script('arguments[0].value="Blorblespack"', input_name)
        input_code = self.driver.find_element("name", self.config['fields']['pas'])
        self.driver.execute_script('arguments[0].value="Smorkleplack"', input_code)
        input_name.submit()
        # self.driver.close()
