from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager


class Browser():
    def __init__(self) -> None:
        self.service = Service(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service = self.service)

    def write_html(self, content):
        with open('source.html', 'w') as file:
            file.write(content)

    def get(self, url, write=False):
        self.driver.get(url)
        print(self.driver.title)

        if write == True:
            self.write_html(self.driver.page_source)
            print("HTML file written")
        
        # self.driver.close()
