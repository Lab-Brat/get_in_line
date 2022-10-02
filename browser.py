import sys
from captcha import Captcha
from PIL import Image
from io import BytesIO
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
        with open('data/_source.html', 'w') as file:
            file.write(self.driver.page_source)
        self.driver.close()

    def get_captcha(self):
        captcha = self.driver.find_element("id", self.config['fields']['cap'])
        location, size = captcha.location, captcha.size
        im = Image.open(BytesIO(self.driver.get_screenshot_as_png()))
        left, top = location['x'], location['y']
        right, bottom = location['x'] + size['width'], location['y'] + size['height']
        im = im.crop((left, top, right, bottom))
        im.save('data/_tmp_screenshot.png')

    def automate(self):
        input_name = self.driver.find_element("name", self.config['fields']['num'])
        self.driver.execute_script(f'arguments[0].value="{self.config["user"]["num"]}"', input_name)
        input_code = self.driver.find_element("name", self.config['fields']['pas'])
        self.driver.execute_script(f'arguments[0].value="{self.config["user"]["pas"]}"', input_code)

        input_captcha = self.driver.find_element("name", self.config['fields']['cap_input'])
        self.get_captcha()
        solver = Captcha('data/_tmp_screenshot.png', write=False)
        input_captcha.send_keys(solver.solve(method='2captcha'))
        input_captcha.send_keys(Keys.ENTER)
        # self.driver.close()
