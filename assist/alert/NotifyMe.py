import playsound

from gtts import gTTS
from plyer import notification
from tkinter import messagebox as msg
import tkinter as tk
from gi.repository import Notify
from assist.utils import helper


def msg_box(title, text, style):
    """
	Style   |   Type        |   Button      |   Return
	------------------------------------------------------
	0           Info            Ok              'ok'
	1           Warning         Ok              'ok'
	2           Error           Ok              'ok'
	3           Question        Yes/No          'yes'/'no'
	4           YesNo           Yes/No          True/False
	5           OkCancel        Ok/Cancel       True/False
	6           RetryCancel     Retry/Cancel    True/False
	"""
    box = [
        msg.showinfo, msg.showwarning, msg.showerror,
        msg.askquestion, msg.askyesno, msg.askokcancel, msg.askretrycancel]
    tk.Tk().withdraw()
    if style in range(7):
        return box[style](title, text)


def playSound(text_to_shout):
    """ play the message """
    obj = gTTS(text=text_to_shout, slow=False, lang='hi')
    flag = True
    while flag:
        try:
            obj.save('eng.mp3')
            flag = False
        except Exception as e:
            print(str(e))
            flag = True
    playsound.playsound("eng.mp3")


def send_notification(title, message, icon=None):
    if helper.CurrentOs == "Linux":
        Notify.init("Assitant")
        notification_obj = Notify.Notification.new(message)
        # notification_obj.add_action(
        #     "action_click",
        #     "Yes",
        #     call_back_fn,
        #     arg
        # )
        # notification_obj.add_action(
        #     "action_click",
        #     "No",
        #     call_back_fn,
        #     arg
        # )
        notification_obj.show()

    else:
        notification.notify(
            title=title,
            message=message,
            app_icon=icon,
            timeout=5
        )


def notify(quiz_info):
    details = list(quiz_info[0].items())[0][1]
    title = list(quiz_info[0].items())[0][0]
    message = f"Sir, There is incomplete quiz with title,  {title}, and Here is some more details, {details}"


# playSound(message)

ICONS = {"danger": "F:\\covid-19\\head.ico"}


class Icons:
    danger = "F:\\covid-19\\head.ico"


def main():
    l = [{'16 June 2020 Percentage Quiz(6.40-8pm)_Bhawana':
              'Attempts allowed: 1\nThis quiz closed on Tuesday, 16 June 2020, 8:00 PM\nTo attempt this quiz you need to know the quiz password\nTime limit: 1 hour 20 mins'},
         {'15 June 2020 Coding Decoding Quiz(6.40-8pm)_Bhawana':
              'Attempts allowed: 1\nThis quiz closed on Monday, 15 June 2020, 8:00 PM\nTo attempt this quiz you need to know the quiz password\nTime limit: 1 hour 20 mins'}]
    notify(l)

    result = msg_box("Test", "some info", 3)
    print(result)


