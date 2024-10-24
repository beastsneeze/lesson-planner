import sqlite3

def init_db():
    connection = sqlite3.connect('db/planner.db')
    cursor = connection.cursor()

    # Create tables for lessons, tasks, and students
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        date TEXT,
        time TEXT,
        subject TEXT,
        notes TEXT,
        completed INTEGER DEFAULT 0,
        default_students INTEGER DEFAULT 0,
        session_price REAL DEFAULT 0.0
    )
    ''')


    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        due_date TEXT,
        status INTEGER DEFAULT 0
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        progress_notes TEXT
    )
    ''')
    add_columns_if_not_exists(cursor)
    connection.commit()
    connection.close()

def add_columns_if_not_exists(cursor):
    cursor.execute("PRAGMA table_info(lessons)")
    columns = [column[1] for column in cursor.fetchall()]

    if 'default_students' not in columns:
        cursor.execute("ALTER TABLE lessons ADD COLUMN default_students INTEGER DEFAULT 0")
    
    if 'session_price' not in columns:
        cursor.execute("ALTER TABLE lessons ADD COLUMN session_price REAL DEFAULT 0.0")


if __name__ == '__main__':
    init_db()
