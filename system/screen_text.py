import pyfiglet
from os import system, name
from random import choice

try:
    from termcolor import colored, cprint
except Exception as e:
    print(e)

color = ['yellow', 'blue', 'green']


def line_sep(t=1):
    for i in range(t):
        cprint('-' * 50, 'magenta')


def asci_banner(msg):
    banner = pyfiglet.figlet_format(msg)
    line_sep(2)
    cprint(banner, choice(color), attrs=['bold'])
    line_sep(2)


def processing(msg):
    cprint('.' * 10 + msg + '.' * 10)


def command_sep():
    cprint('-' * 23 + 'X-X-X' + '-' * 22, 'magenta')


def clear_screen(start=True):
    from settings.setting import START_SCREEN_NAME
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
    if start:
        asci_banner(START_SCREEN_NAME)


if __name__ == '__main__':
    command_sep()
