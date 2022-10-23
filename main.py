import configparser
from browser import Browser

config = configparser.ConfigParser()
config.read('data/_info')

bb = Browser(config, 'trb', mode = 'headless')
# bb.write_html()
bb.automate(method = '2captcha', show=True)
