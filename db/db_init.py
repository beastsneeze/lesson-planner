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
        completed INTEGER DEFAULT 0
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

    connection.commit()
    connection.close()

if __name__ == '__main__':
    init_db()
