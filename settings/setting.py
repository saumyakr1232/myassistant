from system.path import getpath
import os
from termcolor import cprint
from tools.configParser import ConfigParser_manager as CM
from tools.json_manager import JsonManager as JM

all_sections = [
    'bot',
    'default',
    'interaction_setting',
    'cp',
    'template_path',
    'compiler',
    'developer',
    'start_time',
    'browser',
    'directory',
    'credentials'
]


interaction_setting = {
    'voice_reply': True,
    'text_reply': True,
    'voice_read_voice_reply': False,
    'text_read': True
}

bot = {
    'name': 'nobita',
    'gender': 'male',
    'boss': 'Gaurav ',
    'voice_engine': 'pyttsx3', # can change to gTTS (online)
}

directories = {
    'assignment_attachment': None,
    'notes': None
}

credentials = {
    'lms': None,
    'icloud': None
}


DEBUG = True
LEARN = True
BROWSER = 'chrome'
conf_path  = os.path.join(getpath(__file__), 'settings.yaml')

try:
    obj = CM()
    section = 'bot'
    bot = obj.read(conf_path, section=section)
    section = 'interaction_setting'
    x = obj.read(conf_path, section=section)
    for i in interaction_setting:
        if x[i]:
            interaction_setting[i] = True
        else:
            interaction_setting[i]= False
    section = 'developer'
    x = obj.read(conf_path, section=section)
    if x['debug']:
        DEBUG = True
    else:
        DEBUG = False

    if x['learn']:
        LEARN = True
    else:
        LEARN = False

    section = 'browser'
    x = obj.read(conf_path, section=section)

    if x != "":
        BROWSER = x['browser_name']

    section = 'directories'

    x = obj.read(conf_path, section=section)

    if x != '':
        for key in x.keys():
            directories[key] = x[key]

    section = 'credentials'
    x = obj.read(conf_path, section=section)

    if x != "":
        for key in x.keys():
            credentials[key] = x[key]


except Exception as e:
    cprint(e,'red')
    cprint('Setting error.','red')

START_SCREEN_NAME = bot['name']


def update_bot(original_path):
    f = original_path + '/settings/bot.json'
    JM.json_write(f, bot)


def read_bot(original_path):
    f = original_path + '/settings/bot.json'
    bot = JM.json_read(f)
    print(bot)
    # return bot


def update_bot(x):
    global bot
    global START_SCREEN_NAME
    bot = x
    START_SCREEN_NAME = bot['name']


def update_dev(x):
    global DEBUG

    if x['debug']:
        DEBUG = True
    else:
        DEBUG = False

def update_cred(x):
    global credentials
    for key in x.keys():
        credentials[key] = x[key]
    print(credentials)

def update_browser(x):
    global BROWSER
    BROWSER = x['browser_name']

def update_directories(x):
    global  directories
    for key in x.keys():
        directories[key] = directories[key]

if __name__ == '__main__':
    pass




