import requests
import random
import time
import configparser
from browser import Browser

def send_to_telegram(api_token, chat_id, message):
    '''
    Send a message to a Telegram chat.
    '''
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
    sleep_time = random.randint(2, 9)
    sleep_message = f"Next check in {sleep_time} minutes"
    bb = Browser(config, 'trb')
    result = bb.automate(method = '2captcha', show = False)
    print(result)
    if result['result']:
        send_to_telegram(api_token, chat_id, 
                         f"{result['message']}\n{sleep_message}")

    print(f'sleeping for {sleep_time} minutes')
    time.sleep(sleep_time * 60)
