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

def run(time_interval):
    while True:
        sleep_message = f"Next check in {time_interval} minutes"
        bb = Browser(config, 'trb')
        result = bb.automate(method = '2captcha', show = False)
        print(f"{result['message']}timestamp: {result['time']}")
        if result['result']:
            send_to_telegram(api_token, chat_id, 
                            f"{result['message']}\n{sleep_message}")

        print(f'sleeping for {sleep_time} minutes\n')
        time.sleep(sleep_time * 60)


# Read Config file
config = configparser.ConfigParser()
config.read('data/_info')
api_token = config["bot"]["api"]
chat_id = config["bot"]["cid"]

sleep_time = random.randint(2, 5)
run(sleep_time)
