from termcolor import cprint
from models.models import Quiz, Assignment
from dateutil.parser import parse
from datetime import datetime
import random
def quiz_assignment_table(dic: dict):

    column_labels = ["S.NO.", "Title", "Type", "Due Date", "Course"]
    col_width = [0.05, 0.15, 0.15, 0.4, 0.25]

    cell_colors = []
    cell_text = []
    for course in dic.keys():
        items = []
        sub_color = random_color()
        items.extend(dic[course]['quizzes'])
        items.extend(dic[course]['assignments'])
        sno = 1
        for item in items:

            t = "Quiz" if type(item) is Quiz else "Assignment"
            try:
                due_datetime = parse(item.due_date)
            except Exception:
                pass
            due_str = f"{due_datetime.time().hour}:{due_datetime.time().minute} {due_datetime.date()}"
            s = f"{sno}||{item.title}||{t}||{item.due_date}||{course}"
            cell_text.append(s.split("||"))
            sno += 1
            t_color = "magenta" if type(item) is Quiz else "cyan"

            ts_due = due_datetime.timestamp()
            quiz_color = ""
            if due_datetime > datetime.today():
                time_limit = None
                try:
                    time_limit = secs_from_str(item.time_limit)
                except AttributeError as e:
                    pass
                if time_limit is not None:
                    if datetime.now() < datetime.fromtimestamp(ts_due - time_limit):
                        due_color = "green"
                        quiz_color = "on_green"
                    else:
                        due_color = "yellow"
                        quiz_color = 'on_green'
                else:
                    due_color = "green"
                    quiz_color = "on_green"
            else:
                due_color = "red"
                quiz_color = "on_red"

            cell_color = ['palegreen',quiz_color, t_color, due_color, sub_color ]
            cell_colors.append(cell_color)

    title_l = max([len(t[1]) for t in cell_text ])

    max_lengths = [max([len(t[i]) for t in cell_text]) for i in range(len(column_labels))]
    max_lengths[0] = len(column_labels[0])

    column_labels = " | ".join([column_labels[i].center(max([len(t[i]) for t in cell_text])) for i in range(len(column_labels))])
    cprint(column_labels, 'blue')
    for i, text in enumerate(cell_text):
        s_no = text[0]
        s_no = s_no.center(max_lengths[0]) + " | "
        cprint(s_no, 'blue', end="")

        title = text[1].center(max_lengths[1])
        cprint(title, 'cyan',attrs=['bold', 'dark',], end="")
        cprint(" | ", 'blue', end="")

        item_type = text[2].center(max_lengths[2])
        cprint(item_type,cell_colors[i][2] ,end ="")
        cprint(" | ",'blue', end="")

        d_date = text[3].center(max_lengths[3])
        cprint(d_date, cell_colors[i][3], end="")
        cprint(" | ", 'blue', end="")

        item_course = text[4].center(max_lengths[4])
        cprint(item_course, cell_colors[i][4], end="")
        print()


        # row = " | ".join([t.center(max_lengths[i+2]) for i, t in enumerate(text[2:])])
        # cprint(row)

def secs_from_str(time):
    s = time.lower().split()
    secs = 0
    i = 0
    while i < len(s):
        if s[i + 1][0] == 'h':
            secs += int(s[i]) * 3600
            i = i + 1
        else:
            secs += int(s[i]) * 60
            i = i + 1
        i = i + 1

    return  secs

def random_color():
    colors = ['cyan', 'blue', 'magenta', None]
    return random.choice(colors)


if __name__ == '__main__':

    from models.models import Quiz, Assignment
    q1 = Quiz(title="quiz 1", due_date="wednesday 7 april 2021 3:00 pm", course="course 1",time_limit="20 min")
    q2 = Assignment(title="quiz 2", due_date="wednesday 27 april 2021 3:00 pm", course="course 1")
    q3 = Quiz(title="quiz 3", due_date="saturday 24 april 2021 4:00 pm", course="course 2", time_limit="1 hour")
    q4 = Assignment(title="quiz 4", due_date="saturday 24 april 2021 5:00 pm", course="course 1")

    dic = {"course 1":{"quizzes":[q1], "assignments":[q2, q4]}, "course 2": {"quizzes":[q3], "assignments":[]}}

    quiz_assignment_table(dic)

