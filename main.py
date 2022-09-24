import configparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

def write_html(content):
    with open('source.html', 'w') as file:
        file.write(content)

config = configparser.ConfigParser()
config.read('info')

# print webpage title
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service = service)
driver.get(config['url']['ist'])
print(driver.title)

write_html(driver.page_source)
print("HTML file written")
driver.close()
