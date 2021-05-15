from tools.interact import speak
from tools.interact import get_input
from settings.logs import get_logger
from tools.string_processing import string_process
from system.screen_text import asci_banner, line_sep, clear_screen
from settings.setting import START_SCREEN_NAME
from tools.data import google, bye
from AI.ai import ai
import os
from settings._first_load_ import check_if_first_time
logger = get_logger()
def check_done(msg):
    for i in google:
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
                break
            if get == 'clear':
                clear_screen()
            else:
                get = get.strip()
                if get != "" and get != "\n":
                    msg = ai(get)
                    speak(msg)
                    line_sep()

        speak('Good Bye Sir.')
        asci_banner('BYE!')
    else:
        msg = ai(get)
        speak(msg)
        line_sep(t=1)
    logger.debug("Bot stopped.")


if __name__ == '__main__':
    check_if_first_time()
    main()
