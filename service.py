import configparser
import subprocess
import random

class Service:
    def __init__(self):
        pass

    def download_captchas(self, n, link):
        for i in range(n):
            id = random.randint(1, 1001)
            cmd = ['wget', '-O', f'captcha/{i+1}.jpeg', f'{link}{id}']
            subprocess.run(cmd)

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('info')
    service = Service()
    service.download_captchas(5, config['url']['captcha'])
