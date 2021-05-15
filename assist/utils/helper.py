import getpass
import os
import platform
import sys
import time
from wikipedia import wikipedia
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import smtplib
import requests
from selenium.common.exceptions import SessionNotCreatedException
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.chrome.options import Options as OptionsChrome
from selenium.webdriver.firefox.options import Options as OptionFirefox
from pathlib import  Path
import webbrowser
from settings.logs import get_logger
from settings.setting import credentials, update_cred, conf_path, directories, update_directories, \
    BROWSER
from termcolor import cprint
from tools.configParser import ConfigParser_manager as CM

logger = get_logger()
CurrentOs = platform.system()
OsUserName = getpass.getuser()



def getDriverPath(driver='chrome'):
    # Todo optimize getDriverPath
    driver_path = ""
    if driver == 'chrome' and CurrentOs == "Linux":
        driver_path = str(Path(__file__).parent.parent.parent) + '/data/webDrivers/chrome/chromedriver_linux64/chromedriver'
    if driver == 'chrome' and CurrentOs == 'Windows':
        driver_path =  str(Path(__file__).parent.parent.parent) + '/data/webDrivers/chrome/chromedriver_win32/chromedriver.exe'
    if driver == 'firefox' and CurrentOs == "Linux":
        driver_path = str(
            Path(__file__).parent.parent.parent) + '/data/webDrivers/firefox/geckodriver-v0.27.0-linux64/geckodriver'
    if driver == 'firefox' and CurrentOs == "Windows":
        driver_path = str(
            Path(__file__).parent.parent.parent) + '/data/webDrivers/firefox/geckodriver-v0.29.1-win64/geckodriver.exe'
    if os.path.exists(driver_path):
        return  driver_path
    return driver_path

def getMessagesFilePath():
    return str(Path(__file__).parent.parent.parent) + '/data/messages.txt'


def getBrowserDataPath(browser='chrome'):
    """
     Browser User Profile Data
    :param browser: Browser name ex: 'firefox', 'chrome'
    :return: string path
    """
    data_path = ""
    if CurrentOs == "Linux" and browser == 'chrome':
        data_path = f'/home/{OsUserName}/.config/google-chrome/default.'
    if CurrentOs == 'Linux' and browser == 'firefox':
        if os.path.exists(f"/home/{OsUserName}/.mozilla/firefox/"):
            dirs = os.listdir(f"/home/{OsUserName}/.mozilla/firefox/")
            for directory in dirs:
                if directory.split('.').__contains__("default"):
                    data_path = f'/home/{OsUserName}/.mozilla/firefox/{directory}'
    if CurrentOs == 'Windows' and browser == 'chrome':
        data_path = f"C:\\Users\\{OsUserName}\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    if CurrentOs == 'Windows' and browser == 'firefox':
        if os.path.exists(f"C:\\Users\\{OsUserName}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles"):
            dirs = os.listdir(f"C:\\Users\\{OsUserName}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles")
            for directory in dirs:
                if directory.split('.').__contains__("default"):
                    data_path = f'C:\\Users\\{OsUserName}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\{directory}'
    if os.path.exists(data_path):
        return data_path
    else:
        return None

def _load_driver(download_dir=None):
    """
    Load the Selenium driver
    :return: driver
    """
    browserName = BROWSER
    browser_data_path = getBrowserDataPath(browser=browserName)
    web_driver_path = getDriverPath(driver=browserName)
    driver = None
    if browserName.lower() == "firefox":
        option = OptionFirefox()
        if browser_data_path is not None:
            option.add_argument('user-data-dir=' + browser_data_path)
        if download_dir is not None:
            if os.path.exists(download_dir):
                p = {'download.default_directory': download_dir}
                #todo: add download folder here
                pass

            else:
                logger.debug(f"Using default download path {download_dir} doesn't exist")
        try:
            driver = webdriver.Firefox(executable_path=web_driver_path, options=option)
        except InvalidArgumentException:
            print(f"Another Window of {browserName.title()} is open Close it and try again:🤨")
            sys.exit()

    elif browserName.lower() == "chrome":
        option = OptionsChrome()
        option.add_argument('user-data-dir=' + browser_data_path)
        if download_dir is not None:
            if os.path.exists(download_dir):
                p = {'download.default_directory': download_dir}
                option.add_experimental_option('prefs', p)
            else:
                logger.debug(f"Using default download path {download_dir} doesn't exist")
        try:
            driver = webdriver.Chrome(executable_path=web_driver_path, options=option)
        except InvalidArgumentException:
            print(f"Another Window of {browserName.title()} is open Close it and try again:🤨")
            sys.exit()
    return driver


def getWebDriver(download_dir=None):
    # print("webdriver called")
    Driver = None
    try:
        Driver = _load_driver(download_dir)
    except SessionNotCreatedException as e:
        print(e.msg)

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
        return res
    except Exception as e:
        print(e)
        return "Sorry sir"


def website_opener(domain):
    try:
        url = 'https://www.' + domain
        webbrowser.open(url)
        return True
    except Exception as e:
        print(e)
        return False


def get_cred(site: str):
    cred = {}
    obj = CM()
    if credentials[site] is None:
        print()
        cprint(f"{site} credentials are not set please enter :", 'red')
        cprint('Username: ','green' ,end="")
        username = input()
        cred['username'] = username
        cprint('Password: ', 'green', end="")
        password = input()
        cred['password']= password
        obj.update(conf_path, {site:cred}, section='credentials')
        update_cred({site: cred})
        return cred
    else:
        return credentials[site.lower()]

def get_directory(name):
    logger.info("get_directory called")
    path = None
    obj = CM()
    try:
        if directories[name.lower()] is None:
            cprint(f"Sir, you have not specified a directory for {name}", 'red')
            cprint("Please specify directory: ", 'blue', end="")
            d = input()

            try:
                path  = Path(d)
                obj.update(conf_path, {name: str(path.absolute())}, section='directories')
                update_directories({name: str(path.absolute())})
            except Exception as e:
                logger.error(f"Error while getting path {e}")
        else:
            path = Path(directories[name.lower()])
    except KeyError as k:
        logger.error(f"There is no directory for {name}")
    return path


def write_file_from_url(url, file):
    logger.info(f"getting data form {url} and saving into file {file}")
    r = requests.get(url, allow_redirects=True)
    with open(file, 'wb') as file:
        file.write(r.content)


if __name__ == '__main__':
   print(news())