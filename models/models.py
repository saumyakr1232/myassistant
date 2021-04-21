class Course:
    def __init__(self, course_name, course_code):
        self.name = course_name
        self.course_code = course_code

    pass


class Assignment:
    def __init__(self, title, description, start_date, due_date, course):
        self.title = title
        self.description = description
        self.start_date = start_date
        self.due_date = due_date
        self.course = course
        self.is_completed = False


class Quiz(Assignment):
    def __init__(self, title, description, start_date, due_date, course, attempts):
        Assignment.__init__(self, title, description,start_date, due_date, course)
        self.attempts = attempts
        self.score = 0.0
        self.max_score = 0.0


