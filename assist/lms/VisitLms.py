import logging
import os
import pyautogui

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

browserName = "chrome"
webDriverPath = "D:\\Downloads\\chromedriver.exe"
userDataPath = "C:\\Users\\saumy\\AppData\\Local\\Google\\Chrome\\User Data"
driver = webdriver.Chrome(webDriverPath)


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


def copy_assignment_doc(file_name):
	os.chdir(os.getcwd())
	while True:
		try:
			with open(f"C:\\Users\\saumy\\Downloads\\{file_name}", 'rb') as f:
				with open(file_name, "wb") as ff:
					ff.write(f.read())
					return
		except FileNotFoundError:
			time.sleep(2)


def get_incomplete_quizzes():
	# /html/body/div[3]/div[3]/div/div/section/div/div/ul/li[2]/div[3]/ul/li//div/div/div[2]
	# /span/form/div/button/img[contains(@title,'Not completed')]

	# //li//div/div/div[2]/span/form/div/button/img[contains(@title,'Not completed')]

	items = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'quiz')]")))

	print([x.text for x in items])

	incomplete_quizzes = []
	for x in items:
		logger.info(x.text)
		l = x.text.split("\n")
		# title="Not completed: 15 June 2020 Coding Decoding Quiz(6.40-8pm)_Bhawana. Select to mark as complete."
		try:
			print(f"checking:   Not completed: {l[0]}. Select to mark as complete.")
			x.find_element_by_xpath(
				f'//img[contains(@title, \'Not completed: {l[0]}. Select to mark as complete.\')]')
			logger.info("looks incomplete")
			y = x.find_element_by_xpath(".//div[@class='activityinstance']")
			incomplete_quizzes.append(y)
		except NoSuchElementException:
			logger.info("Looks complete")

	return incomplete_quizzes


def get_incomplete_assignments():
	# /html/body/div[3]/div[3]/div/div/section/div/div/ul/li[2]/div[3]/ul/li//div/div/div[2]/span/form/div/button/img[
	# contains(@title,'Not completed')]

	# //li//div/div/div[2]/span/form/div/button/img[contains(@title,'Not completed')]

	items = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,
																				 "//li[contains(@class, 'assign')]")))

	print([x.text for x in items])

	incomplete_assignments = []
	for x in items:
		logger.info(x.text)
		# title="Not completed: Assignment: UNIT 2. Select to mark as complete.
		try:
			x.find_element_by_xpath(
				f'//img[contains(@title, \'Not completed: {x.text}. Select to mark as complete.\')]')
			logger.info("looks incomplete")
			incomplete_assignments.append(x.find_element_by_xpath(".//div[@class='activityinstance']"))
		except NoSuchElementException:
			logger.info("Looks complete")

	return incomplete_assignments


def select_course(title):
	courses_list = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "coursename")))
	print([x.text for x in courses_list])
	i = 1
	for course in courses_list:
		text = str(course.text)
		logger.info(f"Looking for {title} > Attempt :{i}")
		i += 1
		if text.__contains__(title):
			logger.info("Element found")
			course.click()
			break
	return courses_list


def extract_quiz_info():
	logger.info("extract_quiz_info: called")
	quiz_info_elements = WebDriverWait(driver, 20).until(
		EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'box py-3 quizinfo')]")))
	quiz_title_element = WebDriverWait(driver, 20).until(
		EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/div/div/section/div[1]/h2")))
	info = ""
	for element in quiz_info_elements:
		info += element.text
	logger.info(f"information extracted :{info}")
	return {quiz_title_element.text: info}


def extract_assign_info():
	logger.info("extract_assign_info: called")
	assign_info_table = WebDriverWait(driver, 20).until(
		EC.presence_of_element_located((By.XPATH, "//table[@class='generaltable']"))
	)
	assign_title_element = WebDriverWait(driver, 20).until(
		EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/div/div/section/div[1]/h2")))

	assign_document_element = WebDriverWait(driver, 20).until(
		EC.presence_of_element_located((By.XPATH, "//div[@class= 'fileuploadsubmission']//a"))
	)
	try:
		os.remove(f"C:\\Users\\saumy\\Downloads\\{assign_document_element.text}")
	except FileNotFoundError:
		pass
	assign_document_element.click()
	logger.info(f"Document link : {assign_document_element.get_attribute('href')} \n Document Name : {assign_document_element.text}")
	return {assign_title_element.text: assign_info_table.text, "document_link": assign_document_element.get_attribute('href'),
			"document_name": assign_document_element.text}


def login():
	login_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, "Log in")))
	login_btn.click()

	username = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "username")))
	password = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "password")))

	login_btn_final = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "loginbtn")))

	username.send_keys("18scse1010138")
	password.send_keys("Watermelo@1232")
	logger.info("Credentials are set")
	logger.info("log in clicked")
	login_btn_final.click()


def submit_assignment(assignment):
	print(f"HERE {assignment}")
	tabs = driver.window_handles
	driver.switch_to.window(tabs[0])
	time.sleep(5)
	ActionChains(driver).key_down(Keys.CONTROL).click(assignment).key_up(Keys.CONTROL).perform()
	WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
	tabs = driver.window_handles
	driver.switch_to.window(tabs[1])
	submit_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
	submit_button.click()
	upload_arrow = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class= 'dndupload-arrow']")))
	upload_arrow.click()
	time.sleep(5)

	pyautogui.press('tab')
	pyautogui.press('enter')

	for i in range(6):
		pyautogui.press('tab')
	pyautogui.press('enter')
	time.sleep(1)
	pyautogui.write("C:\\Users\\saumy\\PycharmProjects\\assistant\\")
	time.sleep(1)
	pyautogui.press('enter')
	time.sleep(2)
	for i in range(6):
		pyautogui.press('tab')
	pyautogui.write("test.pdf")
	pyautogui.press("enter")
	for i in range(3):
		pyautogui.press('tab')
	pyautogui.press("enter")
	save_changes = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "id_submitbutton")))
	ready = False
	while not ready:
		try:
			save_changes.click()
			ready = True
		except ElementClickInterceptedException :
			ready = False
			time.sleep(2)



def main():
	driver.get("http://lms.galgotiasuniversity.edu.in/")

	login()

	select_course("DEBARRED-Engineering Physics")

	incomplete_quizzes = []
	incomplete_assignments = []
	try:
		incomplete_quizzes = get_incomplete_quizzes()
		incomplete_assignments = get_incomplete_assignments()
	except TimeoutException:
		pass

	print(f"incomplete quiz :{[x.text for x in incomplete_quizzes]}")
	print(f"incomplete assign : {[x.text for x in incomplete_assignments]}")

	quiz_info = []
	assignment_info = []

	for quiz in incomplete_quizzes:
		print(f"HERE : {quiz}")
		print(f"quiz {quiz.text}")
		ActionChains(driver).key_down(Keys.CONTROL).click(quiz).key_up(Keys.CONTROL).perform()

	WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(len(incomplete_quizzes) + 1))
	tabs = driver.window_handles

	for i in range(1, len(tabs)):
		driver.switch_to.window(tabs[i])
		quiz_info.append(extract_quiz_info())
		driver.close()
	driver.switch_to.window(tabs[0])

	print(f"quiz info {quiz_info}")

	for assignment in incomplete_assignments:
		print(f"HERE {assignment}")
		ActionChains(driver).key_down(Keys.CONTROL).click(assignment).key_up(Keys.CONTROL).perform()

	WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(len(incomplete_assignments) + 1))
	tabs = driver.window_handles

	for i in range(1, len(tabs)):
		driver.switch_to.window(tabs[i])
		assignment_info.append(extract_assign_info())
		driver.close()
	# driver.execute_script("window.history.go(-1)")

	print(f"assign info: {assignment_info}")

	for info in assignment_info:
		name = info['document_name']
		copy_assignment_doc(name)

	print("download complete")

	submit_assignment(incomplete_assignments[0])

	try:
		while True:
			pass
	except KeyboardInterrupt:
		print("[*] Exiting...")
		driver.close()


if __name__ == '__main__':
	main()
