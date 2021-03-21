from settings.logs import *
from settings.setting import interaction_setting as it
from settings.setting import bot
from system.screen_text import processing
import random

color = ['blue', 'yellow', 'green']
try:
    from termcolor import colored, cprint
except Exception as e:
    logger.info(str(e))

try:
    import pyttsx3
except Exception as e:
    logger.info(str(e))


def speak_voice_pyttsx3(msg):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 130)
        engine.setProperty('volume', 1)
        engine.say(msg)
        engine.runAndWait()
    except Exception as e:
        logger.info(str(e))


def speak_voice_gtts(msg):
    """
        Convert text to speech using gTTS
        :prams text: text (String)
        :return: True / False (play sound if True otherwise write exception to log and return False)
        """
    try:
        from gtts import gTTS
        import os, playsound
        processing("loading voice from google server, Sir")
        tts = gTTS(text=msg, lang="en")
        logger.debug("Gtts started")
        filename = "voice.mp3"
        flag = True
        while flag:
            try:
                tts.save(filename)
                flag = False
            except ValueError as v:
                print(str(v))
                flag = True
        logger.debug("got audio form gtts, playing the sound")
        playsound.playsound(filename)
        logger.debug('removing audio file')
        os.remove(filename)
        return True
    except Exception as e:
        logger.critical(str(e))
        print("Sorry didn't understand")
        return False


def speak_voice_manager(msg):
    try:
        if bot['voice_engine'] == 'gTTS':
            logger.info('Calling gTTS')
            speak_voice_gtts(msg)
        else:
            logger.info('Calling pyttsx3')
            speak_voice_pyttsx3(msg)
    except Exception as e:
        logger.info(str(e))


def text_output(msg):
    """
    reply in text
    """
    print()
    bot = '(^-^)-> '
    cl = random.choice(color)
    cprint(bot, cl, attrs=['bold'], end="")
    x = msg.capitalize()
    cprint(x, cl)


def speak(msg):
    not_ok = True
    if it['text_reply']:
        text_output(msg)
        not_ok = False
    if it['voice_reply'] or it['voice_read_voice_reply']:
        speak_voice_manager(msg)
        not_ok = False
    if not_ok:
        cprint('Sir your speaking and writing cabapity is disibled. Please enbale it from settings.', 'red')


def get_text_input():
    cprint("command -> ", 'cyan', attrs=['bold'], end='')
    msg = input()
    return msg


def mic_input():
    """
    Fetch input from mic
    return user's voice input as lower text
    """
    try:
        import speech_recognition as sr
        print("Listening")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            cprint('Say something ... ', 'green', attrs=['bold'])
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, phrase_time_limit=6)  # fixme : phrase_time_limit remove it
            try:
                command = r.recognize_google(audio)
                logger.debug(f"you said {command} \n")
            except sr.UnknownValueError:
                logger.error("....")
                command = mic_input()
                return command
            except Exception as e:
                logger.error("Exception: " + str(e))
                return False
        return command.lower()
    except Exception as e:
        logger.info(str(e))
        return get_text_input()


def get_input():
    if it['voice_read_voice_reply']:
        return mic_input()
    elif it['text_read']:
        return get_text_input()
    else:
        logger.error('Your mircrophone audio and read text both are disabled, enable them from settings')
        cprint('Your BOT do not have any listing power, give him the power from settings -_-', 'red', attrs=['bold'])
        return 'NONE'
