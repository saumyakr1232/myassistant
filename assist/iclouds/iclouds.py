import logging
import os
import pyautogui
import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import assist.utils.helper as helper

browserName = "chrome"
webDriverPath = helper.getDriverPath(driver=browserName)
userDataPath = helper.getBrowserDataPath(browser=browserName)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('visitLms.log', 'w')
# c_handler.setLevel(logging.DEBUG)
# f_handler.setLevel(logging.DEBUG)

# formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(formatter)
f_handler.setFormatter(formatter)

# adding handlers to logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)


def login(driver):
    username = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "useriid")))
    password = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "actlpass")))

    login_btn_final = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "psslogin")))

    username.send_keys("18scse1010138\n")
    password.send_keys("Water@1232")
    logger.info("Credentials are set")
    logger.info("log in clicked")
    time.sleep(2)
    login_btn_final.click()


def open_time_table():
    driver = webdriver.Chrome(webDriverPath)
    driver.get("https://gu.icloudems.com/corecampus/index.php")
    login()

    time_table = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                             "(//img[@src='https://corecampus.s3.ap-south-1.amazonaws.com/images/module_images/time-table.svg'])[2]")))

    time_table.click()


def open_attendance(month=None):
    driver = webdriver.Chrome(webDriverPath)
    driver.get("https://gu.icloudems.com/corecampus/index.php")
    login()
    attendance = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                             "(//img[@src='https://corecampus.s3.ap-south-1.amazonaws.com/images/module_images/attendance.svg'])[2]")))
    attendance.click()
    if month:
        # //span[@title='Select Month']
        select_month = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@title='Select Month']")))
        select_month.click()
        # select2-search__field
        select_month_search = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "select2-search__field")))
        select_month_search.send_keys(month + '\n')

    # ti-more-alt
    more_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "ti-more-alt")))
    more_button.click()
    day_wise_attendance = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Day Wise Attendance")))

    course_wise_attendance = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Course Wise Attendance")))

    course_wise_attendance.click()


def login_to_iclouds():
    driver = webdriver.Chrome(webDriverPath)
    driver.get("https://gu.icloudems.com/corecampus/index.php")

    login(driver)


def main():
    driver = webdriver.Chrome(webDriverPath)
    driver.get("https://gu.icloudems.com/corecampus/index.php")

    login()
    open_attendance("september")
    print(driver.page_source)

