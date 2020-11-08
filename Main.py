import datetime
import smtplib
import subprocess
import urllib.request
import requests
import threading
from assist.utils import helper
from time import ctime
import bs4 as bs
import pyautogui
import platform
from assist.note import note
import playsound
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
from assist.calendar import g_calendar
import webbrowser
import random
from assist.whatsapp import monitorWhatsapp, ChatAnalysis
from assist.lms import VisitLms, lms
from assist.iclouds import iclouds

CurrentOs = platform.system()
name = "saumya"

NOTE_STRS = ["make a note", "write this down", "remember this"]
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november",
          "december"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]

CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy", "am i free", "calendar"]
WAKE = "hey tim"
TIME_STRS = ["what's the time", "tell me the time", "what time is it", "what is the time"]


def speak2(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    flag = True
    while flag:
        try:
            tts.save(filename)
            flag = False
        except ValueError as v:
            print(str(v))
            flag = True

    playsound.playsound(filename)


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_audio():
    print("Listening")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source, phrase_time_limit=5)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))
    return said.lower()


def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass
    if month < today.month and month != -1:
        year += 1
    if day < today.day and month == -1 and day != -1:
        month += 1
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()  # 0-6
        diff = day_of_week - current_day_of_week
        print(diff)
        if diff < 0:
            diff += 7
            if text.count("next") >= 1:
                diff += 7
            print(diff)
        return today + datetime.timedelta(diff)
    if month == -1 or day == -1:
        return None
    return datetime.date(month=month, day=day, year=year)


"what do i have planned on september 9th"


def main():
    print("Main.main() called")
    while True:

        text = get_audio()

        if text.count(WAKE) > 0:
            greetings = [f"hey, how can I help you {name}", f"hey, what's up? {name}",
                         f"I'm listening {name}", f"how can I help you? {name}",
                         f"hello {name}"]
            greet = greetings[random.randint(0, len(greetings) - 1)]
            speak(greet)

            for phrase in CALENDAR_STRS:
                if phrase in text:
                    date = get_date(text)
                    if date:
                        for event in g_calendar.get_events(date):
                            speak(event)
                    else:
                        speak("I don't understand")

            for phrase in NOTE_STRS:
                if phrase in text:
                    speak("what would you like me tho write down?")
                    # note_text = get_audio()
                    note_text = "i am the king of the universe"
                    note.note(note_text)
                    speak("I have made a note of that.")

            # Time
            for phrase in TIME_STRS:
                if phrase in text:
                    time = ctime().split(" ")[3].split(":")[0:2]
                    if time[0] == "00":
                        hours = '12'
                    else:
                        hours = time[0]
                    minutes = time[1]
                    time = hours + " hours and " + minutes + "minutes"
                    speak(time)

            # search google
            for phrase in ["search for"]:
                if phrase in text and 'youtube' not in text:
                    search_term = text.split("for")[-1]
                    url = "https://google.com/search?q=" + search_term
                    webbrowser.get().open(url)
                    speak("Here is what I found for" + search_term + "on google")

            for phrase in ["search"]:
                if phrase in text and 'youtube' not in text:
                    search_term = text.replace("search", "")
                    url = "https://google.com/search?q=" + search_term
                    webbrowser.get().open(url)
                    speak("Here is what I found for" + search_term + "on google")

            # search Youtube
            for phrase in ["youtube"]:
                if phrase in text:
                    search_term = text.split("for")[-1]
                    search_term = search_term.replace("on youtube", "").replace("search", "")
                    url = "https://www.youtube.com/results?search_query=" + search_term
                    webbrowser.get().open(url)
                    speak("Here is what I found for " + search_term + "on youtube")

            # get stock price
            for phrase in ["price of"]:
                if phrase in text:
                    search_term = text.split("for")[-1]
                    url = "https://google.com/search?q=" + search_term
                    webbrowser.get().open(url)
                    speak("Here is what I found for " + search_term + " on google")

            # rock paper scissors
            for phrase in ["play game", "rock paper", "start game"]:
                if phrase in text:
                    speak("choose among rock paper or scissor")
                    voice_data = get_audio()
                    moves = ["rock", "paper", "scissor"]

                    cmove = random.choice(moves)
                    pmove = voice_data

                    speak("The computer chose " + cmove)
                    speak("You chose " + pmove)

                    if pmove == cmove:
                        speak("the match is draw")
                    elif pmove == "rock" and cmove == "scissor":
                        speak("Player wins")
                    elif pmove == "rock" and cmove == "paper":
                        speak("Computer wins")
                    elif pmove == "paper" and cmove == "rock":
                        speak("Player wins")
                    elif pmove == "paper" and cmove == "scissor":
                        speak("Computer wins")
                    elif pmove == "scissor" and cmove == "paper":
                        speak("Player wins")
                    elif pmove == "scissor" and cmove == "rock":
                        speak("Computer wins")

            # Toss a coin
            for phrase in ["toss", "toss a coin", "flip", "flip a coin"]:
                if phrase in text:
                    moves = ["head", "tails"]
                    cmove = random.choice(moves)
                    speak("The computer chose " + cmove)

            # calc
            for phrase in ["plus", "minus", "multiply", "divide", "power", "+", "-", "*", "/"]:
                if phrase in text:
                    opr = voice_data.split()[1]

                    if opr == '+':
                        speak(int(voice_data.split()[0]) + int(voice_data.split()[2]))
                    elif opr == '-':
                        speak(int(voice_data.split()[0]) - int(voice_data.split()[2]))
                    elif opr == 'multiply' or 'x':
                        speak(int(voice_data.split()[0]) * int(voice_data.split()[2]))
                    elif opr == 'divide':
                        speak(int(voice_data.split()[0]) / int(voice_data.split()[2]))
                    elif opr == 'power':
                        speak(int(voice_data.split()[0]) ** int(voice_data.split()[2]))
                    else:
                        speak("Wrong Operator")

            # screenshot
            for phrase in ["capture", "my screen", "screenshot"]:
                if phrase in text:
                    myScreenshot = pyautogui.screenshot()
                    myScreenshot.save(f'home/pictures/{datetime.datetime.now()}-screen.png')  # todo
            # wikipedia
            for phrase in ["definition of"]:
                if phrase in text:
                    speak("what do you need the definition of")
                    definition = get_audio()
                    url = urllib.request.urlopen('https://en.wikipedia.org/wiki/' + definition)
                    soup = bs.BeautifulSoup(url, 'lxml')
                    definitions = []
                    for paragraph in soup.find_all('p'):
                        definitions.append(str(paragraph.text))
                    if definitions:
                        if definitions[0]:
                            speak('im sorry i could not find that definition, please try a web search')
                        elif definitions[1]:
                            speak('here is what i found ' + definitions[1])
                        else:
                            speak('Here is what i found ' + definitions[2])
                    else:
                        speak("im sorry i could not find the definition for " + definition)

            # todo:search on wikipedia

            # Current city or region
            for phrase in ["where am i", "my location"]:
                print("here")
                if phrase in text:
                    Ip_info = requests.get('https://api.ipdata.co?api-key=test').json()
                    loc = Ip_info['region']
                    speak(f"You must be somewhere in {loc}")

            # send email
            for phrase in ["send email", "send an email" "email to ", "mail to"]:
                if phrase in text:
                    receiver = text.split("to")[1]
                    speak("Sir, what should i say? ")
                    message = get_audio()
                    try:
                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.ehlo()
                        server.starttls()
                        server.login('Saumyakr181999@gmail.com', 'Password')
                        server.sendmail('Senderemail@gmail.com', receiver, message)
                        server.close()
                        speak("eamil has been sent")
                    except Exception as e:
                        print(str(e))
                        speak("Sorry my friend . I am not able to send this email")
            # login to lms
            for phrase in ['open lms', 'login to lms']:
                if phrase in text:
                    VisitLms.login_to_lms()
                    speak("ready sir,")
            # login ot iclouds
            for phrase in ['open iclouds', 'login to iclouds']:
                if phrase in text:
                    iclouds.login_to_iclouds()
                    speak("opening iclouds sir,")

            # Attendance
            for phrase in ['check attendance', 'open attendance', 'get attendance']:
                if phrase in text:
                    month = text.split("for")
                    month2 = text.split("of")
                    if month in MONTHS:
                        iclouds.open_attendance(month)
                    elif month2 in MONTHS:
                        iclouds.open_attendance(month2)
                    else:
                        iclouds.open_attendance()

            # timetable
            for phrase in ['timetable', 'classes timeing', 'class time', 'schedule', 'time table']:
                if phrase in text:
                    iclouds.open_time_table()

            # open, launch programs
            for phrase in ['launch', 'run']:
                if phrase in text:
                    app = text.split("open")[1].strip()
                    if CurrentOs == "Linux":
                        subprocess.Popen(app)
                    else:
                        subprocess.Popen(f'{app}.exe')
            else:
                speak("Sir, didn't get that part")


if __name__ == '__main__':
    # if helper.isNetworkConnectionAvail():
    #     speak("Welcome back sir,")
    #     speak("should i monitor your whatsapp?")
    #     text = get_audio()
    #     # text = "hmm"
    #     for word in ["yes", "please", "yeah", "hmm"]:
    #         if word in text or word == text:
    #             speak("Which group should i monitor")
    #             answer = get_audio()
    #             # answer = "unofficial sec 4 at level 7"
    #             try:
    #                 group_to_monitor = answer.split("at level")[0]
    #                 level = int(answer.split("at level")[1])
    #                 if group_to_monitor:
    #                     thread_monitor_whatsapp = threading.Thread(target=monitorWhatsapp.monitor_group,
    #                                                                args=(group_to_monitor, 7), daemon=True)
    #                     thread_monitor_whatsapp.start()
    #             except Exception as e:
    #                 print(str(e))
    #                 speak("Sorry, don't understand")

        print("here")
        main()
