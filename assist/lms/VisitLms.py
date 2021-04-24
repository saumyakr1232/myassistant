from settings.logs import logger
import logging
import os
import random
import time
import pyautogui
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, \
    WebDriverException, NoSuchWindowException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tools.string_processing import is_matched
import assist.utils.helper as helper
from models.models import Quiz, Assignment
from UI.table import quiz_assignment_table
from assist.alert.NotifyMe import  msg_box
logger.setLevel(logging.CRITICAL)

def copy_assignment_doc(file_name):
    """
    @param file_name: Location of file
    @type file_name: str
    @return: None
    @rtype: None
    """
    os.chdir(os.getcwd())  # TODO Create a dedicated directory for assignments
    while True:
        try:
            with open(f"C:\\Users\\saumy\\Downloads\\{file_name}", 'rb') as f:
                with open(file_name, "wb") as ff:
                    ff.write(f.read())
                    return
        except FileNotFoundError:
            time.sleep(2)


def get_incomplete_quizzes(driver):
    """
    Search for all incomplete quizzes on course page
    @param driver: Web driver
    @type driver:
    @return: list of  Quiz
    @rtype: list
    """
    logger.debug("get incomplete quizzes called")

    items = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'quiz')]")))

    # print([x.text for x in items])

    incomplete_quizzes = []

    for x in items:
        logger.info(x.text)
        l = x.text.split("\n")

        try:
            # print(f"checking:   Not completed: {l[0]}. Select to mark as complete.")
            x.find_element_by_xpath(
                f'//img[contains(@title, \'Not completed: {l[0]}. Select to mark as complete.\')]')
            logger.info("looks incomplete")
            y = x.find_element_by_xpath(".//div[@class='activityinstance']")
            incomplete_quizzes.append(y)
        except NoSuchElementException:
            logger.info("Looks complete")

    return incomplete_quizzes


def get_incomplete_assignments(driver):
    logger.info("get_incomplete_assignments : called")
    items = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,
                                                                                 "//li[contains(@class, 'assign')]")))
    # print([x.text for x in items])

    incomplete_assignments = []

    for x in items:
        logger.info(x.text)
        # title="Not completed: Assignment: UNIT 2. Select to mark as complete.
        try:
            x.find_element_by_xpath(
                f'//img[contains(@title, \'Not completed: {x.find_element_by_class_name("instancename").text}. Select to mark as complete.\')]')
            logger.info("looks incomplete")
            incomplete_assignments.append(x.find_element_by_xpath('.//div[@class=\'activityinstance\']'))
        except NoSuchElementException:
            logger.info("Looks complete")

    return incomplete_assignments


def select_course(title, driver):
    courses_list = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "coursename")))
    # print([x.text for x in courses_list])
    i = 1
    for course in courses_list:
        text = str(course.text)
        logger.info(f"Looking for {title} > Attempt :{i}")
        i += 1
        if text.__contains__(title):
            logger.info(f"{title} Element found ")
            course.click()
            break
    return courses_list


def _quiz_obj_from_text(title, text, course):
    """
    Convert string to Quiz object
    @param title: Quiz title
    @type title: str
    @param text: description
    @type text: str
    @param course: course name
    @type course: str
    @return: Quiz object
    @rtype: Quiz
    """
    text = text.lower()
    lines = text.split("\n")

    lines = [line.strip() for line in lines if line.strip() != ""]

    quiz = Quiz()
    quiz.title = title
    quiz.course = course
    try:
        attempt_allowed = lines[0].replace("attempts allowed:", "")
        attempt_allowed.strip()
        quiz.attempts = int(attempt_allowed)

        if lines[1].find("until") != -1:
            start_date = lines[1][lines[1].find("until") + 5:].replace(',', "").strip()
            quiz.start_date = start_date
            quiz.time_limit = lines[3].replace("time limit:", " ").strip()
        else:
            quiz.due_date = lines[1][lines[1].find("on") + 2:].replace(',', '').strip()
            quiz.time_limit = lines[2].replace("time limit:", " ").strip()
    except Exception as e:
        logger.error(e)

    return quiz


def extract_quiz_info(driver, course=""):
    """
    Extract Quiz data from quiz page
    @param driver: Web driver
    @type driver:
    @param course: course name
    @type course: str
    @return: Quiz object
    @rtype: Quiz
    """
    logger.info("extract_quiz_info: called")
    quiz_info_elements = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'box py-3 quizinfo')]")))
    quiz_title_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/div/div/section/div[1]/h2")))
    info = ""
    for element in quiz_info_elements:
        info += element.text
    logger.info(f"information extracted :{info}")

    quiz = _quiz_obj_from_text(quiz_title_element.text, info, course)

    return quiz


def _assignment_obj_from_text(title, text, doc_link, doc_name, course):
    """
    Convert text to Assignment Object
    @param title: title of assignment
    @type title: str
    @param text: description of Assignment
    @type text: str
    @param doc_link: url of attachment
    @type doc_link: str
    @param doc_name: name of attachment
    @type doc_name: str
    @param course: course name
    @type course: str
    @return:
    @rtype:
    """
    assignment = Assignment()
    assignment.title = title
    assignment.doc_link = doc_link
    assignment.doc_name = doc_name
    assignment.course = course

    try:
        info_list = text.split("\n")
        assignment.due_date = info_list[3].replace("Due date", '').strip()
    except IndexError as e:
        logger.error(e)

    return assignment


def extract_assign_info(driver, course):
    """
    Fetch assignment data from assignment page
    @param driver: Web driver
    @type driver:
    @param course: Course Name
    @type course: str
    @return: Assignment Object
    @rtype: Assignment
    """
    logger.info("extract_assign_info: called")
    assign_info_table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table[@class='generaltable']"))
    )
    assign_title_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/div/div/section/div[1]/h2")))

    assign_document_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class= 'fileuploadsubmission']//a"))
    )
    try:
        path = helper.get_directory('assignment_attachment')
        duplicate = path / f"{assign_document_element.text}"
        os.remove(duplicate)
        logger.info("duplicate removed")
    except FileNotFoundError:
        logger.debug("no duplicate found")
        pass
    logger.info("saving attachment")
    assign_document_element.click()
    logger.info(
        f"Document link : {assign_document_element.get_attribute('href')} \n Document Name : {assign_document_element.text}")

    return _assignment_obj_from_text(title=assign_title_element.text,
                                     text=assign_info_table.text,
                                     doc_name=assign_document_element.text,
                                     doc_link=assign_document_element.get_attribute('href'),
                                     course=course)


def login(driver):
    """
    Login to galgotias lms
    @param driver: Web driver
    @type driver:
    @return: None
    @rtype:
    """
    logger.debug("login called")
    driver.get('https://lms.galgotiasuniversity.edu.in/login/index.php')
    # login_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, "Log in")))
    # login_btn.click()

    username = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "username")))
    password = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "password")))

    login_btn_final = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "loginbtn")))
    #todo: store id password in setting.yaml
    cred = helper.get_cred('lms')
    username.send_keys(cred['username'])
    password.send_keys(cred["password"])
    logger.debug("Credentials are set")
    logger.debug("log in clicked")
    login_btn_final.click()

#todo: Fix submit_assignment function
def submit_assignment(assignment, driver):
    """
    Submit assignment file on lms
    @param assignment: file uri
    @type assignment: str
    @param driver: web driver
    @type driver:
    @return:
    @rtype:
    """
    logger.debug(f"Submit assignment called with {assignment}")
    tabs = driver.window_handles
    driver.switch_to.window(tabs[0])
    time.sleep(5)
    ActionChains(driver).key_down(Keys.CONTROL).click(assignment).key_up(Keys.CONTROL).perform()
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    tabs = driver.window_handles
    driver.switch_to.window(tabs[1])
    submit_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    submit_button.click()
    upload_arrow = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class= 'dndupload-arrow']")))
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
        except ElementClickInterceptedException:
            ready = False
            time.sleep(2)


def attempt_quiz(driver):
    """
    Attempt a quiz
    @param driver: Web driver
    @type driver:
    @return:
    @rtype:
    """
    questionAnswers = []

    quizLink = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='JDBC (all batches)']")))

    ActionChains(driver).key_down(Keys.CONTROL).click(quizLink).key_up(Keys.CONTROL).perform()
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    tabs = driver.window_handles

    quiz_info = []
    for i in range(1, len(tabs)):
        driver.switch_to.window(tabs[i])
        quiz_info.append(extract_quiz_info(driver))
    attemptButton = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-secondary']")))
    attemptButton.click()
    try:
        startAttemptButton = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@value='Start attempt']")))
        startAttemptButton.click()
    except Exception:
        pass

    for _ in range(1, 25):
        question = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f"//div[@class='qtext']")))
        question = str(question.text)
        # print(f"{_} {question}", "\n*********************************")
        # print("Searching", end="")
        for l in questionAnswers:
            q, a = list(l.items())[0]
            q = str(q)
            q = q.replace(" ", "")
            question = question.replace(" ", "")
            q = q.strip().lower()
            a = a.replace(" ", "")
            a = a.strip().lower()
            # print(".", end="")

            question = question.strip().lower()
            if q == question:
                options = WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//input[@type='radio']/following-sibling::label")))
                for option in options:
                    if str(option.text).strip()[3:].replace(" ", "").lower() == a:
                        try:
                            option.click()
                            break
                        except Exception:
                            i = random.choice(['a. ', 'b. ', 'c. ', 'd. '])
                            answer = WebDriverWait(driver, 20).until(
                                EC.presence_of_element_located((By.XPATH, f"//span[text()='{i}']")))
                            answer.click()
                            # print("Tuukka")
                            break

                else:
                    i = random.choice(['a. ', 'b. ', 'c. ', 'd. '])
                    answer = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, f"//span[text()='{i}']")))
                    answer.click()
                    # print("Tuukka")

                break
        else:
            i = random.choice(['a. ', 'b. ', 'c. ', 'd. '])
            answer = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"//span[text()='{i}']")))
            answer.click()
            # print("Tuukka")
            # print()
        # print()
        try:
            next_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@class,'mod_quiz-next-nav btn')]")))
            next_element.click()
            # print("next")
        except Exception:
            submit0 = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "// input[ @ value = 'Finish attempt ...']")))
            submit0.click()
            submit1 = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//button[text()='Submit all and finish']")))
            submit1.click()
            submit2 = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@class='btn btn-primary']")))
            submit2.click()

    submit0 = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "// input[ @ value = 'Finish attempt ...']")))
    submit0.click()
    submit1 = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Submit all and finish']")))
    submit1.click()
    submit2 = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@class='btn btn-primary']")))
    submit2.click()


def create_report(course, driver):
    """
    Create a map of incomplete assignments and quizzes
    @param course: Course name
    @type course: str
    @param driver: Web driver
    @type driver: driver
    @return: map of assignment and quizzes
    @rtype: dict
    """
    quiz_info = []
    assignment_info = []
    select_course(course, driver)

    incomplete_quizzes_elements = []
    incomplete_assignments = []
    try:
        incomplete_quizzes_elements = get_incomplete_quizzes(driver)
        incomplete_assignments = get_incomplete_assignments(driver)
    except TimeoutException:
        pass

    # print(f"incomplete quiz :{[x.text for x in incomplete_quizzes_elements]}")
    # print(f"incomplete assign : {[x.text for x in incomplete_assignments]}")


    for quiz in incomplete_quizzes_elements:
        ActionChains(driver).key_down(Keys.CONTROL).click(quiz).key_up(Keys.CONTROL).perform()
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(len(incomplete_quizzes_elements) + 1))
    tabs = driver.window_handles

    for i in range(1, len(tabs)):
        driver.switch_to.window(tabs[i])
        quiz_info.append(extract_quiz_info(driver, course))
        driver.close()
    driver.switch_to.window(tabs[0])

    for assignment in incomplete_assignments:
        ActionChains(driver).key_down(Keys.CONTROL).click(assignment).key_up(Keys.CONTROL).perform()

    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(len(incomplete_assignments) + 1))

    tabs = driver.window_handles

    for i in range(1, len(tabs)):
        driver.switch_to.window(tabs[i])
        assignment_info.append(extract_assign_info(driver, course))
        driver.close()
    driver.switch_to.window(tabs[0])

    driver.back()

    return {"quizzes": quiz_info, "assignments": assignment_info}


def get_all_courses(driver):
    """
    Returns all courses from lms
    @param driver: Web driver
    @type driver:
    @return: list of courses
    @rtype: list(str)
    """
    courses = []

    logger.info("get_all_courses : called")
    items = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,
                                                                                 "//h6[@class='d-inline h5']")))
    courses.extend([i.text for i in items])

    return courses


def get_incomplete_assignments_and_quizzes(course=""):
    """
    map all the courses with their incomplete quiz and assignment
    @param course: Course name
    @type course: str
    @return: map of course to incomplete ass and quizzes
    @rtype: dict
    """
    report = {}
    try:
        path = helper.get_directory('assignment_attachment')
        path = str(path.absolute())
        driver = helper.getWebDriver(path)
        driver.get("http://lms.galgotiasuniversity.edu.in/")

        login(driver)

        time.sleep(5)

        all_courses = get_all_courses(driver)
        try:
            all_courses.remove("Student Center")
        except ValueError as e:
            logger.error(e)

        if course != "":
            for c in all_courses:
                if is_matched(course, c.lower(), need=70):
                    report[c] = create_report(c, driver)
                    break
        else:
            for course in all_courses:
                report[course] = create_report(course, driver)
        driver.close()
    except NoSuchWindowException as e:
        logger.error(e.msg)
    except Exception as e:
        logger.error(f"Some error while collecting incomplete quiz/Assignment data {e}")

    finally:
        # msg = helper.beautify_dict(report)
        # msg_box("Incomplete assignment or quizes co")
        quiz_assignment_table(report)
        return report


def main():
    driver = helper.getWebDriver()
    driver.get("http://lms.galgotiasuniversity.edu.in/")

    login(driver)

    time.sleep(5)

    all_courses = get_all_courses(driver)
    all_courses.remove("Student Center")

    report = {}
    for course in all_courses[:2]:
        report[course] = create_report(course, driver)
        time.sleep(5)

    driver.close()

    # for assignment in incomplete_assignments:
    #     print(f"HERE {assignment}")
    #     ActionChains(driver).key_down(Keys.CONTROL).click(assignment).key_up(Keys.CONTROL).perform()
    #
    # WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(len(incomplete_assignments) + 1))
    # tabs = driver.window_handles
    #
    # for i in range(1, len(tabs)):
    #     driver.switch_to.window(tabs[i])
    #     assignment_info.append(extract_assign_info())
    #     driver.close()
    # # driver.execute_script("window.history.go(-1)")
    #
    # print(f"assign info: {assignment_info}")
    #
    # for info in assignment_info:
    #     name = info['document_name']
    #     copy_assignment_doc(name)
    #
    # print("download complete")

    # submit_assignment(incomplete_assignments[0])

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("[*] Exiting...")
        driver.close()


def login_to_lms():
    logger.info("login called")

    driver = helper.getWebDriver()
    driver.get("http://lms.galgotiasuniversity.edu.in/")
    login(driver)
    try:
        while True:
            driver.get_window_rect()
    except WebDriverException:
        print("[*] Exiting...")
    except  KeyboardInterrupt:
        print("[*] Exiting...")
        driver.close()


if __name__ == '__main__':
   r = get_incomplete_assignments_and_quizzes('compiler')
   quiz_assignment_table(r)
   for key in r.keys():
       print(key)
       for ass in r[key]['assignments']:
           print(ass)
       for quiz in r[key]['quizzes']:
           print(quiz)

