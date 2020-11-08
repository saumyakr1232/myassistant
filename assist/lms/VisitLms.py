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


def copy_assignment_doc(file_name):
    """

    :param file_name:
    :return:
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
    # /html/body/div[3]/div[3]/div/div/section/div/div/ul/li[2]/div[3]/ul/li//div/div/div[2]
    # /span/form/div/button/img[contains(@title,'Not completed')]

    # //li//div/div/div[2]/span/form/div/button/img[contains(@title,'Not completed')]

    items = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'quiz')]")))

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


def get_incomplete_assignments(driver):
    logger.info("get_incomplete_assignments : called")
    items = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,
                                                                                 "//li[contains(@class, 'assign')]")))
    print([x.text for x in items])

    incomplete_assignments = []
    for x in items:
        logger.info(x.text)
        # title="Not completed: Assignment: UNIT 2. Select to mark as complete.
        try:
            x.find_element_by_xpath(
                f'//img[contains(@title, \'Not completed: {x.find_element_by_class_name("instancename").text}. Select to mark as complete.\')]')
            logger.info("looks incomplete")
            incomplete_assignments.append(x.find_element_by_xpath(".//div[@class='activityinstance']"))
        except NoSuchElementException:
            logger.info("Looks complete")

    return incomplete_assignments


def select_course(title, driver):
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


def extract_quiz_info(driver):
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


def extract_assign_info(driver):
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
        os.remove(f"C:\\Users\\saumy\\Downloads\\{assign_document_element.text}")
    except FileNotFoundError:
        pass
    assign_document_element.click()
    logger.info(
        f"Document link : {assign_document_element.get_attribute('href')} \n Document Name : {assign_document_element.text}")
    return {assign_title_element.text: assign_info_table.text,
            "document_link": assign_document_element.get_attribute('href'),
            "document_name": assign_document_element.text}


def login(driver):
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


def submit_assignment(assignment, driver):
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
    questionAnswers = [{
        "What happens if you call the method close() on a ResultSet object?": "the database and JDBC resources are released"},
        {
            "Which of the following is an advantage of using PreparedStatement in Java?": "Prevents SQL injection"},
        {"""Connection con=DriverManager.getConnection("jdbc:oracle:thin:@localhost:1521:xe","system","oracle");
________ stmt=con.__________("insert into Emp values(?,?)");
stmt.setInt(1,101);//1 specifies the first parameter in the query
stmt.setString(2,"Ratan");""": "PreparedStatement, prepareStatement"},
        {"How many JDBC driver types does Sun define?": "Four"},
        {
            "Which of the following type of JDBC driver, is also called Type 3 JDBC driver?": "JDBC-Net, pure Java driver"},
        {"The interface ResultSet has a method, getMetaData(), that returns a/an": "Object"},
        {"Which statements about JDBC are true?": "JDBC stands for Java DataBase Connectivity"},
        {
            "Which of the following holds data retrieved from a database after you execute an SQL query using Statement objects?": "ResultSet"},
        {"Which of the following is correct about PreparedStatement?": "Both of the above"},
        {"Which of the following is not a component/class of JDBC API?": "Transaction"},
        {
            "Which of the following methods are needed for loading a database driver in JDBC?": "Both a and b"},
        {"Which of the following is correct about JDBC?": "Both of the above."},
        {"Which of the following is used to limit the number of rows returned?": "setMaxRows(int i)"},
        {"What is the package name of Class?": "java.lang"},
        {"The JDBC-ODBC bridge is": "Multithreaded"},
        {"Which method is used to perform DML statements in JDBC?": "executeUpdate()"},
        {
            "How can you execute a stored procedure in the database?": "Call method execute() on a CallableStatement object"},
        {"Resultset is an interface, how does it support rs.Next()?": """Every vendor of Database provides implementation of ResultSet & other interfaces, through the
Driver"""},
        {
            "Which of the following statements is false as far as different type of statements is concern in JDBC?": "Interim Statement"},
        {"""Which of the following encapsulates an SQL statement which is passed to the database to be parsed, compiled, planned
and executed?""": "Statement"},
        {"""The method on the result set that tests whether or not there remains at least one unfetched tuple in the result set, is said
to be""": "Next method"},
        {"Which type of Statement can execute parameterized queries?": "PreparedStatement"},
        {
            "What happens if you call deleteRow() on a ResultSet object?": """The row you are positioned on is deleted from the ResultSet and from the database"""},
        {
            "Which JDBC driver Type(s) can be used in either applet or servlet code?": "Both Type 3 and Type 4"},
        {"Which packages contain the JDBC classes?": "java.sql and javax.sql"}]

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
        print(f"{_} {question}", "\n*********************************")
        print("Searching", end="")
        for l in questionAnswers:
            q, a = list(l.items())[0]
            q = str(q)
            q = q.replace(" ", "")
            question = question.replace(" ", "")
            q = q.strip().lower()
            a = a.replace(" ", "")
            a = a.strip().lower()
            print(".", end="")

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
                            print("Tukka")
                            break

                else:
                    i = random.choice(['a. ', 'b. ', 'c. ', 'd. '])
                    answer = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, f"//span[text()='{i}']")))
                    answer.click()
                    print("Tukka")

                break
        else:
            i = random.choice(['a. ', 'b. ', 'c. ', 'd. '])
            answer = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"//span[text()='{i}']")))
            answer.click()
            print("Tukka")
            print()
        print()
        try:
            next = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@class,'mod_quiz-next-nav btn')]")))
            next.click()
            print("next")
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
    select_course(course, driver)

    incomplete_quizzes = []
    incomplete_assignments = []
    try:
        incomplete_quizzes = get_incomplete_quizzes(driver)
        # incomplete_assignments = get_incomplete_assignments()
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
        quiz_info.append(extract_quiz_info(driver))
        driver.close()
    driver.switch_to.window(tabs[0])

    print(f"quiz info {quiz_info}")
    driver.back()


def get_all_courses(driver):
    logger.info("get_all_courses : called")
    items = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,
                                                                                 "//h6[@class='d-inline h5']")))
    return [i.text for i in items]


def main():
    driver = webdriver.Chrome(webDriverPath)
    driver.get("http://lms.galgotiasuniversity.edu.in/")

    login(driver)

    print(get_all_courses(driver))
    all_courses = get_all_courses(driver)
    all_courses.remove("Student Center")
    for course in all_courses:
        create_report(course, driver)
        time.sleep(5)

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
    driver = webdriver.Chrome(webDriverPath)
    driver.get("http://lms.galgotiasuniversity.edu.in/")

    login(driver)


if __name__ == '__main__':
    main()
