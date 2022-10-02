import configparser
from browser import Browser

config = configparser.ConfigParser()
config.read('data/_info')

bb = Browser(config, 'trb')
# bb.write_html()
bb.automate()
