import io

from flashtext import KeywordProcessor

from assist.alert import NotifyMe
from assist.lms import VisitLms
from assist.utils import helper


def get_messages():
    with io.open(helper.getMessagesFilePath(), 'r') as f:
        st = f.read()
    return st


def look_for_imp_messages(message_string, keyword_sets):
    """
    :param message_string: Line of text where we will search for keywords
    :param keyword_sets: list of list of keywords
    :return: keywords_extracted (list(str)): List of terms/keywords found in sentence that match our corpus
    """

    kp = KeywordProcessor()
    for keyword_set in keyword_sets:
        kp.add_keywords_from_list(keyword_set)

    return kp.extract_keywords(message_string)


class KeywordSets:
    KeyWordsSet0 = ['book', 'module', 'solution', 'answer', 'notes', 'pdf', 'video', 'result', 'list', 'notice', ]
    keyWordsSet1 = ['theory', 'lecture', 'class', 'lab', 'session', 'practical', ]
    keyWordsSet2 = ['quiz', 'assignment', ]
    keyWordsSet3 = ['lms', 'gulms', 'inpods', 'icloud']
    keyWordsSet4 = ['survey', 'feedback', ]
    keyWordsSet5 = ['vc', 'vc mam', 'mam', 'sir', 'dean', 'dean sir', ]

    keyWordsSet6 = ['present', 'absent', 'attendance', ]
    keyWordsSet7 = ['exam', 'Exam', 'ete', 'mte', 'examination', 'examinations', 'debard', 'detain', 're-appear',
                    're-mte',
                    'debarred', 'detained', 'backpaper', 'test', 'paper', 'mid-term', 'mid term', 'end term',
                    'end-term', 'mandatory', ]
    keyWordsSet8 = ['workshop', 'webinar', 'event', 'competition', 'hackathon', ]

    keyWords = ['date', 'time', 'asap', 'timing', 'today', 'before', 'after', 'soon', ]
    actionsKeyWordsSet = ['fill', 'attempt', 'response', 'attend', 'join', 'watch', 'conduct', 'request', 'share',
                          'accept', ]
    vipKeywords = ['saumya']
    allKeyWordSet = [keyWords, keyWordsSet1, keyWordsSet2, keyWordsSet3, keyWordsSet4, keyWordsSet5, keyWordsSet6,
                     keyWordsSet7, keyWordsSet8]


class Action:
    @staticmethod
    def notification(keyword, group):
        if keyword in KeywordSets.actionsKeyWordsSet or KeywordSets.keyWordsSet3:
            message = f"Sir, Someone mentioned \"{keyword}\" in {group}, would you like to investigate?"
            NotifyMe.send_notification(f"\"{keyword}\" Alert", message)  # todo set ? icon here

        else:
            message = f"SomeOne Mention \"{keyword}\" in {group}"
            NotifyMe.send_notification(f"\"{keyword}\"Alert", message, NotifyMe.ICONS['danger'])

    @staticmethod
    def msg_box(keyword, group):
        if keyword in KeywordSets.actionsKeyWordsSet or KeywordSets.keyWordsSet3:
            message = f"Sir, Someone mentioned \"{keyword}\" in {group}, would you like to investigate?"
            result = NotifyMe.msg_box(f"\"{keyword.title()}\" Alert", message, 4)
            if keyword in KeywordSets.keyWordsSet3 or KeywordSets.keyWordsSet2 or KeywordSets.keyWordsSet3 and result:
                VisitLms


        else:
            message = f"SomeOne Mention \"{keyword}\" in {group}"
            result = NotifyMe.msg_box(f"\"{keyword.title()}\" Alert", message, 0)
            print(result)

    @staticmethod
    def voice_alert(keyword, group):
        if keyword in KeywordSets.actionsKeyWordsSet or KeywordSets.keyWordsSet3:
            message = f"Sir, Someone mentioned \"{keyword}\" in {group}, would you like to investigate?"
            result = NotifyMe.msg_box(f"\"{keyword.title()}\" Alert", message, 4)
            print(result)
            print(type(result))
        else:
            message = f"SomeOne Mention \"{keyword}\" in {group}"
            NotifyMe.playSound(message)


def analyseMessageAndTakeAction(group, level, previous_in_message=None):
    if 0 < level < 8:
        keyword_set_list = KeywordSets.allKeyWordSet[:level]
    else:
        keyword_set_list = [KeywordSets.keyWordsSet2, KeywordSets.actionsKeyWordsSet]
    while True:
        last_in_message = get_messages()
        if last_in_message != previous_in_message:
            print("got some new message")
            previous_in_message = last_in_message
            imp_messages = look_for_imp_messages(last_in_message, keyword_set_list)
            print(imp_messages)
            if len(imp_messages) > 0:
                for message in imp_messages:
                    if helper.is_day():
                        Action.voice_alert(message, group)
                        # time.sleep(180)  # sleep for 3 min after one notification
                    else:
                        Action.msg_box(message, group)
                        # time.sleep(180)


if __name__ == '__main__':
    analyseMessageAndTakeAction("sec 4",
                                4)
