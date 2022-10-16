import sys
from captcha import Captcha
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

        self.field_num = self.config["fields"]["num"]
        self.field_pas = self.config["fields"]["pas"]
        self.field_cap = self.config["fields"]["cap"]
        self.field_cin = self.config["fields"]["cap_input"]
        self.button_nx = self.config["buttons"]["next"]
        self.button_ap = self.config["buttons"]["appl"]

        self.user_num = self.config["user"]["num"]
        self.user_pas = self.config["user"]["pas"]

    def write_html(self):
        with open('data/_source.html', 'w') as file:
            file.write(self.driver.page_source)

    def get_captcha(self):
        captcha = self.driver.find_element("id", self.field_cap)
        location, size = captcha.location, captcha.size
        im = Image.open(BytesIO(self.driver.get_screenshot_as_png()))
        left, right = location['x'], location['x'] + size['width']
        top, bottom = location['y'], location['y'] + size['height']
        im = im.crop((left, top, right, bottom))
        im.save('data/_tmp_screenshot.png')

    def fill_initial_form(self, method):
        input_name = self.driver.find_element("name", self.field_num)
        input_code = self.driver.find_element("name", self.field_pas)  
        self.driver.execute_script(f'arguments[0].value="{self.user_num}"', input_name)
        self.driver.execute_script(f'arguments[0].value="{self.user_pas}"', input_code)

        input_captcha = self.driver.find_element("name", self.field_cin)
        self.get_captcha()
        solver = Captcha('data/_tmp_screenshot.png', write=False)
        input_captcha.send_keys(solver.solve(method=method))
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.button_nx))).click()

    def check_line(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.button_ap))).click()

    def verify_result(self):
        not_found = 'Извините, но в настоящий момент'
        if not_found in self.driver.page_source:
            return ("=================\n"
                    "no luck Boss, please don't be mad :(\n"
                    "=================")
        else:
            return ("=================\n"
                    "an opening FOUND !!!\n"
                    "...\n"
                    "or i'm broken, please fix me\n"
                    "=================\n")

    def automate(self, method='2capcha', show=False):
        self.fill_initial_form(method)
        WebDriverWait(self.driver, 2)
        self.check_line()
        WebDriverWait(self.driver, 2)
        result = self.verify_result()
        self.driver.close()

        if show == True:
            print(result)

        return result
