from assist import assistant
import json
from tools.data import data, youtube, wiki, google, youtube_play, goto_keys, lms_keys, login_keys
from tools.data import install_keys, calc_keys, should_not_learn, version_keys
from tools.data import CALENDAR_STRS, NOTE_STRS, DAYS, MONTHS, DAY_EXTENTIONS, TIME_STRS, DATE_STRS
from tools.data import incomp_ass_quiz_keys
from assist.calendar import g_calendar
from system.install import install, command
from system.screen_text import command_sep
from tools.string_processing import is_matched
from tools.json_manager import JsonManager
from system.Notification import notifyMe
from settings.setting import bot, DEBUG, LEARN
from termcolor import cprint
from settings.config import if_config_type
from system.path import getpath
from settings.config import train_path
from tools.shell import if_shell_type
from tools.run_program_file import if_run_type
from assist.lms import VisitLms
from tools.interact import speak, get_input
import random
import requests
import os
from assist.utils.helper import  get_directory
import threading
import subprocess
import time
import webbrowser
from assist.utils.helper import tell_me_about, getWebDriver, CurrentOs
import pyautogui
import datetime
import multiprocessing

from settings.logs import *

logger = get_logger()
app_id = "AP8UVR-5E83UJJTRX"


def check(msg, mp, need=90):
    logger.debug('check->' + msg)
    for word in mp:
        if is_matched(word, msg, need):
            return True
    return False


def get_date(text):
    # print('date called')
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
                    except ValueError:
                        pass
                    except IndexError:
                        pass
    if month < today.month and month != -1:
        year += 1
    if day < today.day and month == -1 and day != -1:
        month += 1
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()  # 0-6
        diff = day_of_week - current_day_of_week
        # print(diff)
        if diff < 0:
            diff += 7
            if text.count("next") >= 1:
                diff += 7
            # print(diff)
        return today + datetime.timedelta(diff)
    if month == -1 or day == -1:
        return None
    print(str(datetime.date(month=month, day=day, year=year)))
    return datetime.date(month=month, day=day, year=year)


def rep(msg, mp):
    msg = msg.lower()
    for word in mp:
        if word in msg:
            return msg.replace(word, '', 1).strip()
    return msg.strip()


def ai(msg):
    """
    config, setting
    basic questions
    lms_keys
    wiki, youtube, google
    goto
    install, calculate
    screenshot
    calendar
    time, date
    login lms
    get incomp ass / quiz data
    play game (rock paper)
    toss a coin

    """
    logger.debug("called assistant")
    msg = msg.replace('  ', ' ').strip().lower()
    msg.replace(bot['name'], '')
    reply = 'don\'t know what to do sir'

    if if_config_type(msg):
        return 'Good luck sir.'
    try:
        for line in data:
            if is_matched(msg, line, 100):
                reply = data[line]
                return reply
        if check(msg, youtube_play):
            msg = rep(msg, youtube_play)
            logger.info(msg)
            url = "https://www.youtube.com/results?search_query=" + msg
            webbrowser.get().open(url)
            reply = 'Enjoy sir. '

        elif check(msg, goto_keys):
            msg = rep(msg, goto_keys)
            url = "https://" + msg
            webbrowser.get().open(url)
            reply = "Here is what I found for " + msg + "on google"
        elif check(msg, youtube):
            msg = rep(msg, youtube_play)
            logger.info(msg)
            url = "https://www.youtube.com/results?search_query=" + msg
            webbrowser.get().open(url)
            reply = 'Enjoy sir. '
        elif check(msg, wiki):
            msg = rep(msg, wiki)
            reply = tell_me_about(msg)
        elif check(msg, google):
            msg = rep(msg, google)
            url = "https://google.com/search?q=" + msg
            webbrowser.get().open(url)
            reply = "Here is what I found for" + msg + "on google"
        elif check(msg, install_keys):
            msg = rep(msg, install_keys)
            reply = install(msg)
        elif check(msg, ["capture", "my screen", "screenshot"]):
            try:
                myScreenshot = pyautogui.screenshot()
                path = get_directory('screenshot') / f'{datetime.datetime.now().timestamp()}-screenshot.png'
                myScreenshot.save(path)  # todo get proper directory
                reply = 'screen shot saved'
            except Exception as e:
                print(e)
        elif check(msg, CALENDAR_STRS):
            # print("calendar")
            date = get_date(msg)
            if date:
                for event in g_calendar.get_events(date):
                    reply = event
                return reply

            else:
                reply = "Sorry sir, didn't get that"
                return reply
        elif check(msg, calc_keys):
            msg = rep(msg, calc_keys)
            opr = msg.split()[1]
            if opr == '+' or opr == 'plus':
                reply = str(int(msg.split()[0]) + int(msg.split()[2]))
            elif opr == '-' or opr == "minus":
                reply = str(int(msg.split()[0]) - int(msg.split()[2]))
            elif opr == 'multiply' or 'x':
                reply = str(int(msg.split()[0]) * int(msg.split()[2]))
            elif opr == 'divide':
                reply = str(int(msg.split()[0]) / int(msg.split()[2]))
            elif opr == 'power':
                reply = str(int(msg.split()[0]) ** int(msg.split()[2]))
            else:
                reply = "Wrong Operator"
        elif check(msg, TIME_STRS):

            t = time.ctime().split(" ")[3].split(":")[0:2]
            hours = str(abs(12 - int(t[0])))
            minutes = t[1]
            am_pm = "AM" if int(t[0]) < 12 else "PM"
            t = hours + ":" + minutes + " " + am_pm
            reply = f"Sir, time is {t}"
        elif check(msg, DATE_STRS):

            t = time.ctime().split(" ")

            date = t[2]
            month = datetime.date.today().month

            reply = f"Sir, today is {date} {MONTHS[month - 1]}"
        elif check(msg, ["where am i", "my location"]):
            try:
                Ip_info = requests.get('https://geolocation-db.com/json/').json()
                loc = Ip_info['state']
                reply = f"You must be somewhere in {loc}, {Ip_info['country_name']}"
            except Exception:
                reply = "Unable to get your location"

        elif check(msg, ["send email", "send an email" "email to ", "mail to"]):
            reply = "Email feature is not setup yet"
            pass

        elif check(msg, ['launch', 'run']):
            msg = rep(msg, ['launch', 'run'])
            print(msg)
            if CurrentOs == "Linux":
                subprocess.Popen(msg)
            else:
                subprocess.Popen(f'{msg}.exe')
            reply = f"Launching {msg}"

        # specials cases

        elif check(msg, lms_keys):
            d = threading.Thread(name='login_lms', target=VisitLms.login_to_lms)
            d.setDaemon(True)
            d.start()
            reply = "Logging in to lms "

        elif check(msg, incomp_ass_quiz_keys, need=50):

            if msg.find('of') != -1 or msg.find('for') != -1:
                if msg.find('of') != -1:
                    course = msg.split('of')[1].strip()
                else:
                    course = msg.split('for')[1].strip()
                    cprint(f"Sir, Fetching all Incomplete assignments and quizzes of {course}", 'blue')

                VisitLms.get_incomplete_assignments_and_quizzes(course)
                reply = "Done."

            else:
                VisitLms.get_incomplete_assignments_and_quizzes()
                cprint(f"Sir, Fetching all Incomplete assignments and quizzes from lms", 'blue')
                reply = "Done"

        elif check(msg, ["play game", "rock paper", "start game"]):
            speak("Choose among rock, paper and scissor")
            choice = get_input()
            moves = ["rock", "paper", "scissor"]
            cmove = random.choice(moves)
            pmove = choice

            speak("The computer chose " + cmove)
            speak("You chose " + pmove)


            if pmove == cmove:
                reply = "the match is draw"
            elif pmove == "rock" and cmove == "scissor":
                reply = "Player wins"
            elif pmove == "rock" and cmove == "paper":
                reply = "Computer wins"
            elif pmove == "paper" and cmove == "rock":
                reply = "Player wins"
            elif pmove == "paper" and cmove == "scissor":
                reply = "Computer wins"
            elif pmove == "scissor" and cmove == "paper":
                reply = "Player wins"
            elif pmove == "scissor" and cmove == "rock":
                reply = "Computer wins"

        elif check(msg, ["toss a coin", "flip a coin"]):
            moves = ["head", "tails"]
            cmove = random.choice(moves)
            reply = f"Its {cmove.title()}"

        else:
            """ run with arguments """
            if 'cmd:' in msg or '-s' in msg:
                msg = rep(msg, {'cmd:'})
                msg = rep(msg, {'-s'})
                command_sep()
                command(msg.lower())
                command_sep()
                reply = 'done sir'
            else:
                f= None

                try:
                    f = getpath(__file__) + '.learnt'
                    history = JsonManager.json_read(f)
                    for line in history:
                        if is_matched(msg, line, 95):
                            logger.info('Learnt this before')
                            return history[line]

                except FileNotFoundError:
                    logger.error("Can't read history file")

                try:
                    ft = train_path
                    history = JsonManager.json_read(ft)
                    for line in history:
                        if is_matched(msg, line, 95):
                            logger.info('You have trained this before.')
                            return history[line]

                except FileNotFoundError:
                    logger.info("Can't read trained data")
                t = time.time()
                reply = assistant.ask_question(msg)
                t = time.time() - t
                logger.info(str(t) + ' sec')

                ok = True
                for word in should_not_learn:
                    if word in msg.lower() or word in reply.lower():
                        ok = False
                        break
                if ok:
                    logger.info('reply -> ' + reply)
                    if not LEARN:
                        cprint("(Automatically LEARN MODE is disable)Enter y to learn : ", 'red', attrs=['bold'],
                               end='')
                        learn = input('')
                    else:
                        learn = 'y'
                    if learn.lower() == 'y':
                        try:
                            history = JsonManager.json_read(f)
                            history.update({msg: reply})
                            JsonManager.json_write(f, history)
                            logger.info('Learnt')
                        except Exception as e:
                            logger.info("Exception while writing learnt : " + str(e))
        return reply
    except Exception as e:
        logger.error(f"getting some error in ai {e}")
        logger.info('Getting some error in ai')
        logger.info(str(e))
        return reply
