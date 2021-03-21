import datetime
import platform
import random
import smtplib
import subprocess
import threading
import urllib.request
import webbrowser
from time import ctime
import os
# import PySimpleGUI as sg
import bs4 as bs
import playsound
import pyautogui
import pyttsx3
import requests
import speech_recognition as sr
import wikipedia
import wolframalpha
from gtts import gTTS
import sys
from assist.alert import NotifyMe
from assist.calendar import g_calendar
from assist.iclouds import iclouds
from assist.lms import VisitLms
from assist.note import note
from assist.utils import helper
from assist.whatsapp import monitorWhatsapp

CurrentOs = platform.system()
name = "saumya"

NOTE_STRS = ["make a note", "write this down", "remember this"]
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november",
          "december"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]

CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy", "am i free", "calendar"]
WAKE = ["nobita"]
TIME_STRS = ["what's the time", "tell me the time", "what time is it", "what is the time"]
app_id = "AP8UVR-5E83UJJTRX"


def speak2(text):
    """
    Convert text to speech using gTTS
    :prams text: text (String)
    :return: True / False (play sound if True otherwise write exception to log and return False)
    """
    try:
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
        os.remove(filename)
        return True
    except Exception as e:
        print("Sorry didn't understand")
        return False


def shutdown():
    """
    Shutdown assistant, exit the program
    return: True if all goes well False otherwise
    """
    try:
        speak("Good bye. Have a nice day")
        sys.exit()
    except Exception as e:
        print(e)
        return False


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed percent (can go over 100)
    engine.setProperty('volume', 0.9)  # Volume 0-1
    engine.setProperty("voice", 'Mandarin')
    engine.say(text)
    engine.runAndWait()


def mic_input():
    """
    Fetch input from mic
    return user's voice input as lower text
    """
    print("Listening")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something ... ')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source, phrase_time_limit=6)  # fixme : phrase_time_limit remove it
        try:
            command = r.recognize_google(audio)
            print(f"you said {command} \n")
        except sr.UnknownValueError:
            print("....")
            command = mic_input()
            return command
        except Exception as e:
            print("Exception: " + str(e))
            return False
    return command.lower()


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

    client = wolframalpha.Client(app_id)

    while True:
        sg.theme('DarkPurple')
        layout = [[sg.Text('Enter a command'), sg.InputText()], [sg.Button('Ok'), sg.Button('Cancel')]]
        window = sg.Window('Assistant', layout)
        got_answer = False
        # text = get_audio()
        event, values = window.read()
        if event in (None, 'Cancel'):
            break

        window.close()
        text = values[0] + " nobita"
        print(text)
        for wake_word in WAKE:
            if wake_word == text.strip():
                greetings = [f"hey, how can I help you {name}", f"hey, what's up? {name}",
                             f"I'm listening {name}", f"how can I help you? {name}",
                             f"hello {name}"]
                greet = greetings[random.randint(0, len(greetings) - 1)]
                speak(greet)
            else:
                for phrase in CALENDAR_STRS:
                    phrase.strip()
                    if phrase in text:
                        date = get_date(text)
                        if date:
                            for event in g_calendar.get_events(date):
                                speak(event)
                                got_answer = True
                        else:
                            speak("I don't understand")

                for phrase in NOTE_STRS:  # ["make a note", "write this down", "remember this"]
                    if phrase in text:
                        speak("what would you like me tho write down?")

                        layout = [[sg.Text('Note text'), sg.InputText()], [sg.Button('Ok'), sg.Button('Cancel')]]
                        window = sg.Window('Notes', layout)

                        event, values = window.read()
                        if event in (None, 'Cancel'):
                            break

                        window.close()
                        note_text = values[0]

                        # note_text = get_audio()
                        note.note(note_text)
                        speak("I have made a note of that.")
                        got_answer = True

                # Time
                for phrase in TIME_STRS:  # ["what's the time", "tell me the time", "what time is it", "what is the time"]
                    if phrase in text:
                        time = ctime().split(" ")[4].split(":")[0:2]
                        if time[0] == "00":
                            hours = '12'
                        else:
                            hours = time[0]
                        minutes = time[1]
                        time = hours + " hours and " + minutes + "minutes"
                        speak(time)
                        got_answer = True

                # search google
                for phrase in ["search for"]:
                    if phrase in text and 'youtube' not in text:
                        search_term = text.split("for")[-1].replace("nobita", "")
                        url = "https://google.com/search?q=" + search_term
                        webbrowser.get().open(url)
                        speak("Here is what I found for" + search_term + "on google")
                        got_answer = True

                # search Youtube
                for phrase in ["youtube"]:
                    if phrase in text:
                        search_term = text.split("for")[-1]
                        search_term = search_term.replace("on youtube", "").replace("search", "")
                        url = "https://www.youtube.com/results?search_query=" + search_term
                        webbrowser.get().open(url)
                        speak("Here is what I found for " + search_term + "on youtube")
                        got_answer = True

                # get stock price
                for phrase in ["price of"]:
                    if phrase in text:
                        search_term = text.split("for")[-1]
                        url = "https://google.com/search?q=" + search_term
                        webbrowser.get().open(url)
                        speak("Here is what I found for " + search_term + " on google")
                        got_answer = True

                # rock paper scissors
                for phrase in ["play game", "rock paper", "start game"]:
                    if phrase in text:
                        speak("choose among rock paper or scissor")
                        text = mic_input()
                        moves = ["rock", "paper", "scissor"]

                        cmove = random.choice(moves)
                        pmove = text

                        speak("The computer chose " + cmove)
                        speak("You chose " + pmove)
                        got_answer = True

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
                for phrase in ["toss a coin", "flip a coin"]:
                    if phrase in text:
                        got_answer = True
                        moves = ["head", "tails"]
                        cmove = random.choice(moves)
                        speak("The computer chose " + cmove)

                # calc
                for phrase in ["plus", "minus", "multiply", "divide", "power", "+", "-", "*", "/"]:
                    if phrase in text:
                        got_answer = True
                        opr = text.split()[1]

                        if opr == '+' or opr == 'plus':
                            speak(int(text.split()[0]) + int(text.split()[2]))
                        elif opr == '-' or opr == "minus":
                            speak(int(text.split()[0]) - int(text.split()[2]))
                        elif opr == 'multiply' or 'x':
                            speak(int(text.split()[0]) * int(text.split()[2]))
                        elif opr == 'divide':
                            speak(int(text.split()[0]) / int(text.split()[2]))
                        elif opr == 'power':
                            speak(int(text.split()[0]) ** int(text.split()[2]))
                        else:
                            speak("Wrong Operator")

                # screenshot
                for phrase in ["capture", "my screen", "screenshot"]:
                    if phrase in text:
                        got_answer = True
                        myScreenshot = pyautogui.screenshot()
                        myScreenshot.save(f'{datetime.datetime.now()}-screen.png')  # todo get proper directory
                # wikipedia
                if "definition of" in text:
                    definition_of = text.split("definition of")
                    helper.tell_me_about(definition_of)
                if "tell me about" in text:
                    topic = text.split("tell me about")
                    helper.tell_me_about(topic)

                # Current city or region
                for phrase in ["where am i", "my location"]:

                    if phrase in text:
                        got_answer = True
                        Ip_info = requests.get('https://api.ipdata.co?api-key=test').json()
                        loc = Ip_info['region']
                        speak(f"You must be somewhere in {loc}")

                # send email
                for phrase in ["send email", "send an email" "email to ", "mail to"]:
                    if phrase in text:
                        got_answer = True
                        receiver = text.split("to")[1]
                        speak("Sir, what should i say? ")
                        message = mic_input()
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
                        got_answer = True
                        VisitLms.login_to_lms()
                        speak("ready sir,")
                # login ot iclouds
                for phrase in ['open iclouds', 'login to iclouds']:
                    if phrase in text:
                        got_answer = True
                        iclouds.login_to_iclouds()
                        speak("opening iclouds sir,")

                # Attendance
                for phrase in ['check attendance', 'open attendance', 'get attendance']:
                    if phrase in text:
                        got_answer = True
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
                        got_answer = True
                        iclouds.open_time_table()

                # open, launch programs
                for phrase in ['launch', 'run']:
                    if phrase in text:
                        got_answer = True
                        app = text.split("open")[1].strip()
                        if CurrentOs == "Linux":
                            subprocess.Popen(app)
                        else:
                            subprocess.Popen(f'{app}.exe')

                # wolfram
                if not got_answer:
                    try:
                        # fixme: rethink this
                        text = text.replace(WAKE[0], "")
                        wolfram_res = next(client.query(text).results).text
                        # wiki_res = wikipedia.summary(text, sentences=2)
                        # speak(wolfram_res)
                        # NotifyMe.msg_box(title="Wikipedia Result", text=wiki_res, style=0)
                        NotifyMe.msg_box(title="wolfram result", text=wolfram_res, style=0)
                    except wikipedia.exceptions.DisambiguationError:
                        wolfram_res = next(client.query(text).results).text
                        # speak(wolfram_res)
                        NotifyMe.msg_box(title="wolfram result", text=wolfram_res, style=0)
                    except wikipedia.exceptions.PageError:
                        wolfram_res = next(client.query(text).results).text
                        # speak(wolfram_res)
                        NotifyMe.msg_box(title="Wolfarm result", text=wolfram_res, style=0)
                    except:
                        print("some error occured")
                        speak("Sorry, sir some error occured")


if __name__ == '__main__':
    if helper.isNetworkConnectionAvail():
        speak("Welcome back sir, should i monitor your whatsapp?")
        # text = get_audio()
        text = "hmm"
        for word in ["yes", "please", "yeah", "hmm"]:
            if word in text or word == text:
                speak("Which group should i monitor")
                # answer = get_audio()
                answer = "unofficial sec 4 at level 7"
                try:
                    group_to_monitor = answer.split("at level")[0]
                    level = int(answer.split("at level")[1])
                    print(f"group to monitor :{group_to_monitor}, level: {level}")
                    if group_to_monitor:
                        thread_monitor_whatsapp = threading.Thread(target=monitorWhatsapp.monitor_group,
                                                                   args=(group_to_monitor, 7), daemon=True)
                        thread_monitor_whatsapp.start()
                except Exception as e:
                    print(str(e))
                    speak("Sorry, don't understand")
                    break

    main()
