from fuzzywuzzy import fuzz
from settings.logs import get_logger

logger = get_logger()


def match_string(msg, original, no=1):
    if no == 1:
        return max(fuzz.WRatio(msg, original), fuzz.token_sort_ratio(msg, original))
    elif no == 2:
        return fuzz.WRatio(msg, original)
    elif no == 3:
        return fuzz.ratio(msg, original)
    else:
        return fuzz.token_sort_ratio(msg, original)


def is_matched(msg, original, need=90, no=1):
    percentage = match_string(msg, original, no)
    # logger.debug(msg + ' '+original+' ' +str(percentage) )
    return True if percentage >= need else False


def string_process(msg):
    lt = list(msg.split())
    msg = ' '.join(lt)
    return msg.lower()


def wiki_string(msg):
    data = ['wiki', 'wikipedia', 'what', 'is', 'tell', 'me', 'about', 'information', 'give', 'who']
    msg = msg.split()
    key = ''
    for w in msg:
        if w not in data:
            key += w + ' '

    return key.strip()


if __name__ == '__main__':
    print(string_process("how aer   you   my borhter : aldfj ;"))