import sqlite3

def init_db():
    connection = sqlite3.connect('db/planner.db')
    cursor = connection.cursor()

    # Create tables for lessons, tasks, and students
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        day_of_week TEXT NOT NULL,
        time TEXT NOT NULL,
        subject TEXT NOT NULL,
        notes TEXT,
        completed INTEGER DEFAULT 0,
        default_students INTEGER DEFAULT 0,
        session_price REAL DEFAULT 0.0
    )
    ''')

    connection.commit()
    connection.close()
    




init_db()
