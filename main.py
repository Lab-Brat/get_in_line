import configparser
from captcha import Captcha
from browser import Browser

config = configparser.ConfigParser()
config.read('info')

bb = Browser(config)
bb.get(write=False)
