from tools.configParser import ConfigParser_manager as CM
from system.path import getpath
import os
from termcolor import cprint

positive = ['yes', '1', 'true']

compiler = {
    "c++": "g++ '{filename}' -o '{executable}' && ./'{executable}'",
    "c++ debug": "g++ -std=c++17 -O2 -DPAUL -Wshift-overflow=2  -Wshadow  -Wall '{filename}' -o '{executable}' && "
                 "./'{executable}'",
    "python": "python3 '{filename}'",

}

template_path = {
    'c++': '/media/saurav/Programming/GIthub/Code-Lab/geany/ai_template.cpp',
    'python': '/media/saurav/Programming/GIthub/Code-Lab/geany/ai_template.py',
}
cf_tool_mode = False

DEBUG = True

conf_path = os.path.join(getpath(__file__), 'settings.yaml')

try:
    obj = CM()
    section = 'template_path'
    x = obj.read(conf_path, section=section)

    template_path['c++'] = x['cpp']
    template_path['python'] = x['python']

    section = 'compiler'
    x = obj.read(conf_path, section)

    compiler['c++'] = x['cpp']
    compiler['c++ debug'] = x['cpp_debug']
    compiler['python'] = x['python']

    section = 'developer'
    x = obj.read(conf_path, section=section)

    if x['debug']:
        DEBUG = True
    else:
        DEBUG = False


except Exception as e:
    print(e)
    cprint("Settings error.", 'red')


def update_tp(x):
    global template_path
    template_path = x


def update_compiler(x):
    global compiler
    compiler = x

