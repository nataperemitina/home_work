import os.path as Path
import sqlite3

SQL_INSERT_TASK = 'INSERT INTO calendar (title, description, due_date) VALUES (?,?,?)';

SQL_UPDATE_TASK_STATUS = '''
    UPDATE calendar SET status_id=? WHERE id=?
'''

SQL_UPDATE_TASK_TITLE = '''
    UPDATE calendar SET title=? WHERE id=?
'''

SQL_UPDATE_TASK_DESCRIPTION = '''
    UPDATE calendar SET description=? WHERE id=?
'''

SQL_UPDATE_TASK_DUE_DATE = '''
    UPDATE calendar SET due_date=? WHERE id=?
'''

SQL_SELECT_ALL = '''
    SELECT 
        calendar.id, title, description, due_date, task_status.status as status
    FROM calendar LEFT JOIN task_status ON calendar.status_id = task_status.id;
'''

SQL_SELECT_ALL_SHORT = '''
    SELECT 
        calendar.id, title, description, due_date
    FROM calendar 
'''

SQL_SELECT_TASK_BY_STATUS = SQL_SELECT_ALL_SHORT + ' WHERE status_id=?'

SQL_SELECT_TASK_BY_PK = SQL_SELECT_ALL_SHORT + ' WHERE id=?'

def connect(db_name=None):
    if db_name is None:
        db_name = ':memory:'

    conn = sqlite3.connect(db_name)
    return conn

def initialize(conn):
    script_path = Path.join(Path.dirname(__file__), 'schema.sql')

    with conn, open(script_path) as f:
        conn.executescript(f.read())

def get_all(conn):
    with conn:
        cursor = conn.execute(SQL_SELECT_ALL)
        return cursor.fetchall()

def get_opened(conn):
    with conn:
        cursor = conn.execute(SQL_SELECT_TASK_BY_STATUS, (1,))
        return cursor.fetchall()

def get_task(conn, id):
    with conn:
        cursor = conn.execute(SQL_SELECT_TASK_BY_PK, (id,))
        return cursor.fetchone()

def add_task(conn, title, desc, due_date):
    if not title:
        raise RuntimeError("Task title can't be empty.")

    with conn:
        cursor = conn.execute(SQL_INSERT_TASK, (title, desc, due_date,))
        pk = cursor.lastrowid
        
        cursor = conn.execute(SQL_SELECT_TASK_BY_PK, (pk,))
        
        return cursor.fetchone()


def update_task_title(conn, id, title):
    if not title:
        raise RuntimeError("Task title can't be empty.")

    with conn:
        conn.execute(SQL_UPDATE_TASK_TITLE, (title, id,))

def update_task_description(conn, id, desc):
    with conn:
        conn.execute(SQL_UPDATE_TASK_DESCRIPTION, (desc, id,))

def update_task_due_date(conn, id, due_date):
    with conn:
        conn.execute(SQL_UPDATE_TASK_DUE_DATE, (due_date, id,))

def complete_task(conn, id):
    with conn:
        conn.execute(SQL_UPDATE_TASK_STATUS, (2,id,))

def reopen_task(conn, id):
    with conn:
        conn.execute(SQL_UPDATE_TASK_STATUS, (1,id,))
