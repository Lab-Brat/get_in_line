import sys
import datetime
from captcha import Captcha
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager


class Browser():
    def __init__(self, config, destination, mode = 'normal'):
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
        self.options = Options()
        if mode == 'headless':
            self.options.headless = True
        self.driver  = webdriver.Firefox(options = self.options, 
                                         service = self.service)
        self.driver.get(url)

        self.field_num = self.config["fields"]["num"]
        self.field_pas = self.config["fields"]["pas"]
        self.field_cap = self.config["fields"]["cap"]
        self.field_cin = self.config["fields"]["cap_input"]
        self.button_nx = self.config["buttons"]["next"]
        self.button_ap = self.config["buttons"]["appl"]

        self.user_num = self.config["user"]["num"]
        self.user_pas = self.config["user"]["pas"]

    def write_html(self, filename):
        '''
        Write currently open web page to an html file.
        '''
        with open(f'data/{filename}', 'w') as file:
            file.write(self.driver.page_source)

    def get_captcha(self):
        '''
        Save captcha from the webpage locally.
        '''
        captcha = self.driver.find_element("id", self.field_cap)
        location, size = captcha.location, captcha.size
        im = Image.open(BytesIO(self.driver.get_screenshot_as_png()))
        left, right = location['x'], location['x'] + size['width']
        top, bottom = location['y'], location['y'] + size['height']
        im = im.crop((left, top, right, bottom))
        im.save('data/_tmp_screenshot.png')

    def fill_initial_form(self, method):
        '''
        Fill in application number and code,
        solve captcha (from get_captcha) and submit form.
        '''
        input_name = self.driver.find_element("name", self.field_num)
        input_code = self.driver.find_element("name", self.field_pas)  
        self.driver.execute_script(f'arguments[0].value="{self.user_num}"', input_name)
        self.driver.execute_script(f'arguments[0].value="{self.user_pas}"', input_code)

        input_captcha = self.driver.find_element("name", self.field_cin)
        self.get_captcha()
        solver = Captcha('data/_tmp_screenshot.png', write=False)
        input_captcha.send_keys(solver.solve(method=method))
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.button_nx))).click()

    def check_line(self):
        '''
        Click on the verification button after form submission.
        '''
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.button_ap))).click()

    def verify_result(self):
        '''
        Check if an appointment date is available.
        '''
        not_found = '????????????????, ???? ?? ?????????????????? ????????????'
        if not_found in self.driver.page_source:
            return {"result": False, 
                    "message": "no luck :(\n",
                    "time": datetime.datetime.now().strftime("%H:%M:%S")}
        else:
            self.write_html('_login_success.html')
            return {"result": True, 
                    "message": "an opening FOUND !!!\n",
                    "time": datetime.datetime.now().strftime("%H:%M:%S")}

    def automate(self, method='2capcha', show=False):   
        '''
        Run above methods in sequence to obtain a result.
        '''
        result = None
        tries  = 0
        while result is None and tries <= 5:
            try:
                self.fill_initial_form(method)
                WebDriverWait(self.driver, 2)
                self.check_line()
                WebDriverWait(self.driver, 2)
                result = self.verify_result()
                if result["result"] == False:
                    self.driver.close()
            except:
                print("Couldn't get the result, retrying...")
                tries += 1
                self.driver.find_element("name", self.field_num).clear()
                self.driver.find_element("name", self.field_pas).clear()
                self.driver.find_element("name", self.field_cin).clear()

        if show == True:
            print(result)

        if tries >= 4:
            result = {"result": False, 
                      "message": "Exeded maxium retry count\n",
                      "time": datetime.datetime.now().strftime("%H:%M:%S")}
            self.driver.close()

        return result
