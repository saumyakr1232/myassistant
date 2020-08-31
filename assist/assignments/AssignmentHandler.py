import PyPDF2
from bs4 import BeautifulSoup
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import webbrowser as wb
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


def read_pdf(path):
    pdfFileObj = open(path, 'rb')

    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    pages = pdfReader.numPages

    text = ""

    for page in range(pages):
        pageObj = pdfReader.getPage(page)
        text += pageObj.extractText()

    pdfFileObj.close()


def answer(driver, question):
    url = "https://www.google.com/search?q=" + question
    driver.get(url)
    elements = driver.find_elements_by_xpath("//span[@class = 'e24Kjd']")
    for element in elements:
        print(element.text)
    time.sleep(20)


def main():
    print(convert_pdf_to_txt("../../Assignment2-optics.pdf"))
    url = "https://www.google.com/search?q=" + "Describe the formation of Newton rings in reflected monochromatic light"
    res = requests.get(url)
    html_page = res.content

    soup = BeautifulSoup(html_page, 'html.parser')

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    # print(text)

    # browserName = "chrome"
    # webDriverPath = "D:\\Downloads\\chromedriver.exe"
    # userDataPath = "C:\\Users\\saumy\\AppData\\Local\\Google\\Chrome\\User Data"

    # driver = webdriver.Chrome(webDriverPath)
    # answer(driver, "Describe the formation of Newton rings in reflected monochromatic light")
    bad_answer = text.split("monthPast yearAll resultsAll")[1]
    print(bad_answer[16:])


if __name__ == '__main__':
    main()
