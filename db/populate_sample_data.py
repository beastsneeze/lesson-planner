import sqlite3
import random
from faker import Faker

# Initialize Faker for generating random data
fake = Faker()

# Function to populate the database with sample data
def populate_database():
    connection = sqlite3.connect('db/planner.db')  # Update with your actual database name
    cursor = connection.cursor()
    
    # Day and subject options
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    subjects = ["Math", "Science", "History", "Geography", "Art", "Computer Science", "English"]
    
    # Generate 50 sample records
    for _ in range(50):
        title = fake.sentence(nb_words=3)
        day_of_week = random.choice(days_of_week)
        time = f"{random.randint(8, 17):02}:{random.randint(0, 59):02}"  # Random time from 08:00 to 17:59
        subject = random.choice(subjects)
        notes = fake.paragraph(nb_sentences=2)
        completed = random.randint(0, 1)
        default_students = random.randint(5, 20)
        session_price = round(random.uniform(20.0, 100.0), 2)
        
        # Insert the record into the database
        cursor.execute('''
            INSERT INTO lessons (title, day_of_week, time, subject, notes, completed, default_students, session_price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, day_of_week, time, subject, notes, completed, default_students, session_price))
    
    # Commit and close the connection
    connection.commit()
    connection.close()
    print("Database populated with sample data.")

# Run the function to populate the database
populate_database()
