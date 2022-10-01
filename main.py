import configparser
from captcha import Captcha
from browser import Browser

config = configparser.ConfigParser()
config.read('info')

url = config['url']['trb']
bb = Browser()
bb.get(url, write=False)
