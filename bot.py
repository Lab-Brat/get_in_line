import requests
import random
import time
import configparser
from browser import Browser

def send_to_telegram(api_token, chat_id, message):
    apiURL = f'https://api.telegram.org/bot{api_token}/sendMessage'
    try:
        response = requests.post(apiURL, json={'chat_id': chat_id, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)


# Read Config file
config = configparser.ConfigParser()
config.read('data/_info')
api_token = config["bot"]["api"]
chat_id = config["bot"]["cid"]

# Run bot
while True:
    bb = Browser(config, 'trb')
    result = bb.automate(method = '2captcha', show = False)
    send_to_telegram(api_token, chat_id, result)

    sleep_time = random.randint(9, 52)
    print(f'sleeping for {sleep_time} minutes')
    time.sleep(sleep_time * 60)
