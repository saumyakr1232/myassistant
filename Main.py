from tools.interact import speak
from tools.interact import get_input
from settings.logs import *
from tools.string_processing import string_process
from system.screen_text import asci_banner, line_sep, clear_screen
from settings.setting import START_SCREEN_NAME
from AI.data import GOOGLE, bye
from AI.ai import ai
import os


def check_done(msg):
    for i in GOOGLE:
        if i in msg:
            return False
    for i in bye:
        if i in msg:
            return True
    return False


def main(get="", original_path=""):
    logger.debug('Assistant start at ' + str(os.getcwd()))
    asci_banner(START_SCREEN_NAME)
    if get == '':
        speak("Hello sir, how can i help you?")

        while True:

            get = string_process(get_input())
            print()
            if check_done(get):
                break;
            if get == 'clear':
                clear_screen()
            else:
                msg = ai(get)
                speak(msg)
                line_sep()
        speak('Good Bye Sir.')
        asci_banner('BYE!')
    else:
        msg = ai(get)
        speak(msg)
        line_sep(t=2)
    logger.debug("Bot stopped.")


if __name__ == '__main__':
    main()
