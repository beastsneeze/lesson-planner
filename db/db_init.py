import sqlite3
from datetime import datetime, timedelta

def init_db():
    connection = sqlite3.connect('db/planner.db')
    cursor = connection.cursor()

    # Create the lessons table with start_time and end_time columns
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

    # Check if `start_time` and `end_time` columns already exist, and if not, rename and modify as needed
    cursor.execute("PRAGMA table_info(lessons)")
    columns = [column[1] for column in cursor.fetchall()]

    # Step 1: Rename `time` to `start_time` if `start_time` doesn't already exist
    if 'start_time' not in columns:
        cursor.execute("ALTER TABLE lessons RENAME COLUMN time TO start_time")

    # Step 2: Add the `end_time` column if it doesn't already exist
    if 'end_time' not in columns:
        cursor.execute("ALTER TABLE lessons ADD COLUMN end_time TEXT")

    # Step 3: Set `end_time` to be one hour after `start_time` for each record
    cursor.execute("SELECT id, start_time FROM lessons")
    lessons = cursor.fetchall()

    for lesson_id, start_time in lessons:
        # Parse the start time and add 1 hour
        try:
            start_dt = datetime.strptime(start_time, "%H:%M")
            end_dt = start_dt + timedelta(hours=1)
            end_time = end_dt.strftime("%H:%M")
            
            # Update the record with the calculated end_time
            cursor.execute("UPDATE lessons SET end_time = ? WHERE id = ?", (end_time, lesson_id))
        except ValueError:
            print(f"Invalid time format for lesson ID {lesson_id}. Expected 'HH:MM'.")

    connection.commit()
    connection.close()

init_db()
