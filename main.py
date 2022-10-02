import configparser
from browser import Browser

config = configparser.ConfigParser()
config.read('info')

bb = Browser(config, 'ist')
bb.write_html()
# bb.automate()
