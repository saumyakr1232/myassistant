import getpass
import os
import platform
import sys
import time
from pathlib import Path
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import smtplib
import requests
import yaml
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.chrome.options import Options as OptionsChrome
from selenium.webdriver.firefox.options import Options as OptionFirefox
import wikipedia
import re
import webbrowser

CurrentOs = platform.system()
OsUserName = getpass.getuser()





def getCred(portal="lms"):
    with open(str(Path(__file__).parent) + "/userData.yaml", "r") as f:
        docs = yaml.load(f, Loader=yaml.FullLoader)
    return docs[portal]


def getDriverPath(driver='chrome'):
    if driver == 'chrome' and CurrentOs == "Linux":
        return str(Path(__file__).parent.parent.parent) + '/data/webDrivers/chrome/chromedriver_linux64/chromedriver'
    if driver == 'chrome' and CurrentOs == 'Windows':
        return str(Path(__file__).parent.parent.parent) + '/data/webDrivers/chrome/chromedriver_win32/chromedriver.exe'
    if driver == 'firefox' and CurrentOs == "Linux":
        return str(
            Path(__file__).parent.parent.parent) + '/data/webDrivers/firefox/geckodriver-v0.27.0-linux64/geckodriver'
    if driver == 'firefox' and CurrentOs == "Windows":
        return str(
            Path(__file__).parent.parent.parent) + '/data/webDrivers/firefox/geckodriver-v0.27.0-win64/geckodriver.exe'


def getMessagesFilePath():
    return str(Path(__file__).parent.parent.parent) + '/data/messages.txt'


def getBrowserDataPath(browser='chrome'):
    """
     Browser User Profile Data
    :param browser: Browser name ex: 'firefox', 'chrome'
    :return: string path
    """

    if CurrentOs == "Linux" and browser == 'chrome':
        return f'/home/{OsUserName}/.config/google-chrome/default.'
    if CurrentOs == 'Linux' and browser == 'firefox':
        dirs = os.listdir(f"/home/{OsUserName}/.mozilla/firefox/")
        for directory in dirs:
            if directory.split('.').__contains__("default"):
                return f'/home/{OsUserName}/.mozilla/firefox/{directory}'
    if CurrentOs == 'Windows' and browser == 'chrome':
        return f"C:\\Users\\{OsUserName}\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    if CurrentOs == 'Windows' and browser == 'firefox':
        dirs = os.listdir(f"/home/{OsUserName}/.mozilla/firefox/")
        for directory in dirs:
            if directory.split('.').__contains__("default"):
                return f'C:\\Users\\{OsUserName}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\{directory}'


def _load_driver():
    """
    Load the Selenium driver
    :return: driver
    """
    with open(str(Path(__file__).parent) + "/userData.yaml", "r") as f:
        docs = yaml.load(f, Loader=yaml.FullLoader)

    browserName = docs['browserPref']
    browser_data_path = getBrowserDataPath(browser=browserName)
    web_driver_path = getDriverPath(driver=browserName)
    driver = None
    if browserName.lower() == "firefox":
        option = OptionFirefox()
        option.add_argument('user-data-dir=' + browser_data_path)
        try:
            driver = webdriver.Firefox(web_driver_path, options=option)
        except InvalidArgumentException:
            print(f"Another Window of {browserName.title()} is open Close it and try again:🤨")
            sys.exit()

    elif browserName.lower() == "chrome":
        option = OptionsChrome()
        option.add_argument('user-data-dir=' + browser_data_path)
        try:
            driver = webdriver.Chrome(web_driver_path, options=option)
        except InvalidArgumentException:
            print(f"Another Window of {browserName.title()} is open Close it and try again:🤨")
            sys.exit()
    return driver


def getWebDriver():
    print("webdriver called")
    Driver = _load_driver()
    return Driver


def is_day():
    if 8 < time.localtime().tm_hour < 20:
        return True
    else:
        return False


def news():
    try:
        news_url = "https://news.google.com/news/rss"
        Client = urlopen(news_url)
        xml_page = Client.read()
        Client.close()
        soup_page = soup(xml_page, "xml")
        news_list = soup_page.findAll("item")
        li = []

        for news in news_list:
            li.append(str(news.title.text.encode('utf-8'))[1:])
            return li
    except Exception as e:
        print(e)
        return False


def send_email(sender_email, sender_password, receiver_email, msg):
    try:
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(sender_email, sender_password)
        mail.sendmail(sender_email, receiver_email, msg)
        mail.close()
        return True
    except Exception as e:
        print(e)
        return False


def tell_me_about(topic):
    try:
        ny = wikipedia.page(topic)
        res = str(ny.content[:500].encode('utf-8'))
        res = re.sub('[^a-zA-Z.\d\s]', '', res)[1:]
        return res
    except Exception as e:
        print(e)
        return False


def website_opener(domain):
    try:
        url = 'https://www.' + domain
        webbrowser.open(url)
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    print(news())


