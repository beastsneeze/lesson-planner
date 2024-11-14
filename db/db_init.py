import sqlite3
from datetime import datetime, timedelta

def init_db():
    connection = sqlite3.connect('db/planner.db')
    cursor = connection.cursor()

    # Create the lessons table with the specified columns
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        day_of_week TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        subject TEXT NOT NULL,
        notes TEXT,
        completed INTEGER DEFAULT 0,
        default_students INTEGER DEFAULT 0,
        session_price REAL DEFAULT 0.0
    )
    ''')

    # Commit changes and close the connection
    connection.commit()
    connection.close()

# Call the init_db function to create the table
init_db()

