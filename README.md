### get_in_line
#### About
Automate checking the status of an online application.  
Stack: Python, Selenium, OpenCV, PyTesseract, 2captcha.  
<br/>
In a nutshell, `Selenium` opens Firefox browser, fills out required fields in a form, 
solves captcha either locally with OCR (<30% accuracy), 
or using 2captcha online captcha solver(99% accuracy), 
clicks `Enter` and gets the resut.  
Result is then sent to the user with Telegram.

#### Set up
##### VM
On the VM where this program will be deployed it's best to have a GUI,
becuase when positive result is returned the browser is left opened for user 
to choose a date.  
It's very easy to install XFCE desktop on Ubuntu 22.04 server:
```
apt update && apt upgrade -y
apt install -yq xfce4-session xfce4-goodies
apt install xinit xrdp
useradd -m linechecker
passwd linechecker
*enter a strong password for user (>20 letters and symbols)
```
Reboot server after installation, and connect via RDP to the newly create user.

##### Browser
Program works with the Fierfox browser, therefore it has to be installed as well. 
By default Ubuntu ships with snap version of Firefox, but Selenium doesn't 
support it yet, so it should be deleted and reinstalled from the repository.
Steps: 
```
snap remove firefox
add-apt-repository ppa:mozillateam/ppa
echo '
Package: *
Pin: release o=LP-PPA-mozillateam
Pin-Priority: 1001
' | sudo tee /etc/apt/preferences.d/mozilla-firefox
echo 'Unattended-Upgrade::Allowed-Origins:: "LP-PPA-mozillateam:${distro_codename}";' | sudo tee /etc/apt/apt.conf.d/51unattended-upgrades-firefox
apt install firefox
```

##### Config
Config file at `data/_info` should be prepared with following fields:
** Omitted for privacy concerns, will be added in the future

##### Dependencies
First set virtual environment, and then install dependencies:
```
apt install -yq python3-pip python3-venv
cd get-in-line
python3 -m pip venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

#### Run
For one time use run `main.py`:
```
python3 main.py
```
If you get a bot key from BotFather, then run `bot.py`:
```
python bot.py
```
