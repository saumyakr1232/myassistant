class Course:
    def __init__(self, course_name, course_code):
        self.name = course_name
        self.course_code = course_code

    pass


class Assignment:

    def __init__(self, title="", doc_link="", doc_name= "", start_date="", due_date="", course=""):
        self.title = title
        self.doc_link = doc_link
        self.doc_name = doc_name
        self.start_date = start_date
        self.due_date = due_date
        self.course = course
        self.is_completed = False

    def __str__(self):
        return f"""
               title: {self.title}
               start_date: {self.start_date}
               due_date: {self.due_date}
               course: {self.course}
               dco link: {self.doc_link}
               doc_name: {self.doc_name}
               """


class Quiz:
    def __init__(self, title="", start_date="", due_date="", course="", attempts=1, time_limit = 0):
        self.title = title
        self.start_date = start_date
        self.due_date = due_date
        self.course = course
        self.attempts = attempts
        self.time_limit = time_limit
        self.score = 0.0
        self.max_score = 0.0

    def __str__(self):
        return f"""
               title: {self.title}
               start_date: {self.start_date}
               due_date: {self.due_date}
               course: {self.course}
               attempts allowed: {self.attempts}
               time limits: {self.time_limit}
               """
