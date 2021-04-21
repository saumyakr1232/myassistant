import sqlite3
from sqlite3 import Error
import logging
from models.models import Course, Assignment, Quiz

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('database.log', 'w')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(formatter)
f_handler.setFormatter(formatter)

# adding handlers to logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)


def create_connection(db_file):
    """
    Create a database connection to a sqlite database
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        logger.debug(f"{db_file} connection success")
    except Error as e:
        logger.error(e)

    return conn


def create_table(conn, create_table_sql):
    """
    create a table form a create table sql statement
    """

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        logger.error(e)


def init_database():
    conn = create_connection(r"S:\Projects\myassistant\data\database.db")
    table_courses = """
    CREATE TABLE IF NOT EXISTS courses (
        course_code text PRIMARY KEY,
        name text NOT NULL
    )
    """

    table_assignments = """
    CREATE TABLE IF NOT EXISTS assignments (
        id integer PRIMARY KEY,
        title text NOT NULL,
        description text NOT NULL,
        start_date text,
        due_date text NOT NULL,
        course_id text NOT NULL,
        is_completed integer DEFAULT 0,
        FOREIGN KEY (course_id) REFERENCES courses(course_code)
    )
    """
    table_quizzes = """
        CREATE TABLE IF NOT EXISTS quizzes (
            id integer PRIMARY KEY,
            title text NOT NULL,
            description text NOT NULL,
            start_date text,
            due_date text NOT NULL,
            course_id text NOT NULL,
            attempts integer,
            score REAL DEFAULT 0,
            max_score REAL default 0,
            FOREIGN KEY (course_id) REFERENCES courses(course_code)
        )
        """

    if conn:
        create_table(conn, table_courses)
        create_table(conn, table_assignments)
        create_table(conn, table_quizzes)
    else:
        logger.error("cannot create the database connection")


def create_courses(conn, course):
    sql = f"""
        INSERT INTO courses (name, course_code) 
        VALUES(\"{course.name}\", "{course.course_code}")
    """

    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid


def create_assignment(conn, assignment):
    """

    """

    sql = f"""
        INSERT INTO assignments(title, description, start_date, due_date, course_id)
        VALUES ("{assignment.title}", "{assignment.description}",
         "{assignment.start_date}","{assignment.due_date}", "{assignment.course}")
    """

    curr = conn.cursor()
    curr.execute(sql)
    conn.commit()
    return curr.lastrowid


def create_quiz(conn, quiz):
    """

    """

    sql = f"""
        INSERT INTO quizzes (title, description, start_date, due_date, course_id, attempts, score, max_score)
        VALUES ("{quiz.title}", "{quiz.description}",
         "{quiz.start_date}","{quiz.due_date}", "{quiz.course}", {quiz.attempts},
         {quiz.score}, {quiz.max_score})
    """

    curr = conn.cursor()
    curr.execute(sql)
    conn.commit()
    return curr.lastrowid

