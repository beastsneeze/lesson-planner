from models.lesson import Lesson
from models.task import Task
import sqlite3

def show_menu():
    print("\n--- Lesson Planner Menu ---")
    print("1. Add a new lesson")
    print("2. View all lessons")
    print("3. Mark lesson as complete")
    print("4. Add a new task")
    print("5. View all tasks")
    print("6. Mark task as complete")
    print("0. Exit")

def main():
    while True:
        show_menu()
        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_lesson()
        elif choice == "2":
            view_lessons()
        elif choice == "3":
            mark_lesson_complete()
        elif choice == "4":
            add_task()
        elif choice == "5":
            view_tasks()
        elif choice == "6":
            mark_task_complete()
        elif choice == "0":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")
def add_lesson():
    title = input("Enter lesson title: ")
    date = input("Enter lesson date (YYYY-MM-DD): ")
    time = input("Enter lesson time (HH:MM): ")
    subject = input("Enter lesson subject: ")
    notes = input("Enter lesson notes (optional): ")

    # Create the Lesson object
    new_lesson = Lesson(title, date, time, subject, notes)

    # Insert into the database
    connection = sqlite3.connect('db/planner.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO lessons (title, date, time, subject, notes, completed) VALUES (?, ?, ?, ?, ?, ?)",
                   (new_lesson.title, new_lesson.date, new_lesson.time, new_lesson.subject, new_lesson.notes, new_lesson.completed))
    connection.commit()
    connection.close()

    print(f"Lesson '{new_lesson.title}' added successfully!")

def view_lessons():
    connection = sqlite3.connect('db/planner.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM lessons")
    lessons = cursor.fetchall()

    if lessons:
        print("\n--- All Lessons ---")
        for lesson in lessons:
            print(f"ID: {lesson[0]}, Title: {lesson[1]}, Date: {lesson[2]}, Time: {lesson[3]}, Subject: {lesson[4]}, Completed: {bool(lesson[5])}")
    else:
        print("No lessons found.")

    connection.close()
def mark_lesson_complete():
    lesson_id = input("Enter the ID of the lesson to mark as complete: ")

    connection = sqlite3.connect('db/planner.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE lessons SET completed = 1 WHERE id = ?", (lesson_id,))
    connection.commit()
    connection.close()

    print(f"Lesson {lesson_id} marked as complete!")
def add_task():
    description = input("Enter task description: ")
    due_date = input("Enter due date (YYYY-MM-DD): ")

    new_task = Task(description, due_date)

    connection = sqlite3.connect('db/planner.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO tasks (description, due_date, status) VALUES (?, ?, ?)",
                   (new_task.description, new_task.due_date, new_task.status))
    connection.commit()
    connection.close()

    print(f"Task '{new_task.description}' added successfully!")

def view_tasks():
    connection = sqlite3.connect('db/planner.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    if tasks:
        print("\n--- All Tasks ---")
        for task in tasks:
            print(f"ID: {task[0]}, Description: {task[1]}, Due Date: {task[2]}, Status: {'Complete' if task[3] else 'Incomplete'}")
    else:
        print("No tasks found.")

    connection.close()
def mark_task_complete():
    task_id = input("Enter the ID of the task to mark as complete: ")

    connection = sqlite3.connect('db/planner.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE tasks SET status = 1 WHERE id = ?", (task_id,))
    connection.commit()
    connection.close()

    print(f"Task {task_id} marked as complete!")


main()