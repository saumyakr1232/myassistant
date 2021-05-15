import wolframalpha
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError
from itertools import cycle
from tools.string_processing import is_matched
import sys
import webbrowser
import time
from threading import Thread
from assist.utils.decorators import debug
from settings.logs import get_logger
logger = get_logger()

api_id = "AP8UVR-5E83UJJTRX"

wolframalpha_client = wolframalpha.Client(app_id=api_id)

done = False

def check(msg, mp, need=90):
    for word in mp:
        if is_matched(word, msg, need):
            return True

def ask_question(question):
    logger.debug("ask_question called")
    global done
    result = None


    try:
        if check(question, ['definition', 'define', 'wikipedia', 'wiki', 'ask wiki']) or len(question.split(" ")) in [1,2]:
            result = wikipedia.summary(question, sentences=1)
    except PageError:
        pass
    except DisambiguationError:
        pass

    if result is None or result == "":
        logger.debug("looking in wolfarm alpha")
        result = ask_wolframalpha(question)




    if result is None:
        logger.debug("googling")
        url = "https://google.com/search?q=" + question
        webbrowser.get().open(url)
        result = "Googling.. Check Browser"

    done = True
    print()



    return result

def animate():
    for c in cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rThinking.. ' + c)
        sys.stdout.flush()
        time.sleep(0.1)



def ask_wolframalpha(question):
    try:
        wolfram_res = next(wolframalpha_client.query(question).results).text
    except StopIteration:
        return None
    return wolfram_res


if __name__ == '__main__':
    print(ask_question("dsalfk nasldk asldkfj in patna"))


