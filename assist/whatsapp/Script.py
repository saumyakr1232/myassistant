from selenium.common.exceptions import InvalidArgumentException
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options as OptionsChrome
from selenium.webdriver.firefox.options import Options as OptionFirefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from assist.utils.decorators import debug
import time
from datetime import datetime
import sys
import io
# from autoGui import bring_forward

from assist.whatsapp import ChatAnalysis


@debug
def set_things_up(browser_name, web_driver_path, user_data_path):
    """
    set global variables
    :param browser_name: Name of browser (ex: firefox)
    :param web_driver_path: webDriver path
    :param user_data_path: path of user-data directory for the browser
    :return:
    """
    values = {
        'browser_name': browser_name,
        'web_driver_path': web_driver_path,
        'user_data_path': user_data_path,
    }
    return values


@debug
def load_driver(values):
    """
    Load the Selenium driver based on driver
    :param values: Dictionary returned by set_thing_up method
    :return: driver
    """

    driver = None
    if str(values['browser_name']).lower() == "firefox":
        option = OptionFirefox()
        option.add_argument('user-data-dir=' + str(values['user_data_path']))
        try:
            driver = webdriver.Firefox(str(values['web_driver_path']), options=option)
        except InvalidArgumentException:
            print(f"Another Window of {values['browser_name'].title()} is open Close it and try again:🤨")
            sys.exit()

    elif str(values['browser_name']).lower() == "chrome":
        option = OptionsChrome()
        option.add_argument('user-data-dir=' + str(values['user_data_path']))
        try:
            driver = webdriver.Chrome(str(values['web_driver_path']), options=option)
        except InvalidArgumentException:
            print(f"Another Window of {values['browser_name'].title()} is open Close it and try again:🤨")
            sys.exit()
    else:
        print(str(values["browser_name"]) + "is not supported : try \"chrome\" or \"firefox\"")
    return driver


@debug
def search_chat(driver, name):
    """
    Function search for the user and open his chat
    :param driver: web_driver
    :param name: name of person or group
    :return:
    """

    # global group_title
    group_title = None
    x_arg = f'//span[@title="{name}"]'
    try:
        if EC.presence_of_element_located((By.XPATH, x_arg)) and EC.staleness_of((By.XPATH, x_arg)):
            group_title = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((
                By.XPATH, x_arg)))
            print(group_title.text)
        else:
            print("Element not located waiting for 5 sec")
            time.sleep(5)
            group_title = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((
                By.XPATH, x_arg)))
            print(group_title.text)
    except TimeoutException:
        print("Time out exception waiting for 10 secs")
        time.sleep(10)
        if EC.presence_of_element_located((By.XPATH, x_arg)) and EC.staleness_of((By.XPATH, x_arg)):
            group_title = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((
                By.XPATH, x_arg)))
            print(group_title.text)
        else:
            print("Element no located waiting for 5 sec")
            time.sleep(5)
            group_title = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((
                By.XPATH, x_arg)))
            print(group_title.text)
    finally:
        if group_title is not None:
            group_title.click()


@debug
def get_every_chat(driver):
    elements = None
    elements1 = None
    chats = []
    try:
        elements = driver.find_elements_by_class_name("_3CneP")
        elements1 = driver.find_elements_by_class_name("_25Ooe")

    finally:
        for e in elements:
            chats.append(e.text)

        for e in elements1:
            chats.append(e.text)
        return chats


@debug
def read_unread_messages(driver, now):
    """
    Reading the unread message
    :param now:
    :param driver:
    :return:
    """
    print("read_unread_message : called " + now)
    MessageString = ""
    emojis = []

    for messages in driver.find_elements_by_xpath("//div[contains(@class,'message-in')]"):
        MessageString += str(messages.text) + "\n"
        try:
            message_container = messages.find_element_by_xpath(
                ".//div[@class='copyable-text']")
            # MessageString = MessageString + str(message_container.find_element_by_xpath(
            # 	".//span[contains(@class,'selectable-text invisible-space copyable-text')]"
            # ).text) + "\n"

            for emoji in message_container.find_elements_by_xpath(
                    ".//img[contains(@class,'selectable-text invisible-space copyable-text')]"):
                emojis.append(emoji.get_attribute("data-plain-text"))

        except NoSuchElementException:
            try:
                time.sleep(5)
                message_container = messages.find_element_by_xpath(
                    ".//div[@class='copyable-text']")

                for emoji in message_container.find_elements_by_xpath(
                        ".//img[contains(@class,'selectable-text invisible-space copyable-text')]"
                ):
                    emojis.append(emoji.get_attribute("data-plain-text"))
            except NoSuchElementException:
                pass
            except StaleElementReferenceException:
                pass
    print(datetime.now().strftime("%H:%M:%S") + "\n END")
    return MessageString, emojis


# .//button[contains(@class, '_19mFZ')]
@debug
def writeMessagesToLocal(last_in_message, emojis, previous_in_message=None):
    if last_in_message != previous_in_message:
        with io.open("../../data/messages.txt", "w") as f:
            messages = last_in_message.split("\n")
            try:
                for m in messages:
                    f.write(str(m))
                    f.write("\n")
            except UnicodeEncodeError:
                m = m.encode('utf-8')
                f.write(str(m))
                f.write("\n")
                print("Unicode char")
            for emoji in emojis:
                try:
                    emoji = emoji.encode('utf-8')
                    f.write(str(emoji))
                    f.write("$\t")
                except UnicodeEncodeError:
                    print("unable to write emojis" + emoji)
            f.write("####################################################")
        print(last_in_message, emojis)


@debug
def main():
    browserName = "chrome"
    webDriverPath = "/home/storage/saumya/PycharmProjects/assistant/webDrivers/chrome/chromedriver_linux64/chromedriver"
    userDataPath = "/home/saumyakr1232/.config/google-chrome/default."

    value = set_things_up(browserName, webDriverPath, userDataPath)
    driver = load_driver(value)
    driver.get("https://web.whatsapp.com/")
    try:
        # bring_forward("script.py")
        print("hello world")
    except Exception :
        print("some error occurred")
    chats = []
    while len(chats) == 0:
        time.sleep(2)
        chats = get_every_chat(driver)
        chats = list(dict.fromkeys(chats))
    print("Select one from Recent chats ")
    x = 1
    for i in chats:
        print(f"{x}. {i}")
        x += 1
    choice = int(input("Enter your choice here :👉  "))

    search_chat(driver, chats[choice - 1])
    previous_in_message = None
    while True:
        last_in_message, emojis = read_unread_messages(driver, datetime.now().strftime("%H:%M:%S"))

        writeMessagesToLocal(last_in_message, emojis, previous_in_message)
        previous_in_message = last_in_message

        time.sleep(2)
        ChatAnalysis.analyseMessageAndTakeAction(choice, [ChatAnalysis.KeywordSets.keyWordsSet2],
                                                 ChatAnalysis.Action.msg_box)


if __name__ == '__main__':
    main()
