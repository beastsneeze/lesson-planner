# from models.lesson import Lesson
# from models.task import Task
# import sqlite3
# from datetime import datetime
# from db.db_init import init_db, add_columns_if_not_exists


# def validate_date(date_str):
#     try:
#         # Ensures date is in YYYY-MM-DD format
#         datetime.strptime(date_str, '%Y-%m-%d')
#         return True
#     except ValueError:
#         return False

# def validate_time(time_str):
#     try:
#         # Ensures time is in HH:MM format
#         datetime.strptime(time_str, '%H:%M')
#         return True
#     except ValueError:
#         return False

# def validate_id(input_str):
#     # Check if the input is a positive integer
#     return input_str.isdigit()

# def get_db_connection():
#     return sqlite3.connect('db/planner.db')

# def db_init():
#     # Initialize the database and update schema if necessary
#     connection = sqlite3.connect('db/planner.db')
#     cursor = connection.cursor()

#     # Initialize the database
#     init_db()

#     # Add new columns if they do not exist
#     add_columns_if_not_exists(cursor)

#     # Continue with the rest of your application logic
#     connection.commit()
#     connection.close()

# def menu():
#     while True:
#         print("\n--- Lesson Planner Menu ---")
#         print("1. Add a new lesson")
#         print("2. Update a lesson")
#         print("3. View all lessons")
#         print("4. Mark lesson as complete")
#         print("5. Delete a lesson")
#         print("6. Add a new task")
#         print("7. Update a task")
#         print("8. View all tasks")
#         print("9. Mark task as complete")
#         print("10. Delete a task")
#         print("0. Exit")

#         choice = input("\nEnter your choice: ")

#         if choice == "1":
#             add_lesson()
#             view_lessons()
#         elif choice == "2":
#             view_lessons()
#             update_lesson()
#         elif choice == "3":
#             view_lessons()
#         elif choice == "4":
#             view_lessons()
#             mark_lesson_complete()
#         elif choice == "5":
#             view_lessons()
#             delete_lesson()
#         elif choice == "6":
#             add_task()
#             view_tasks()
#         elif choice == "7":
#             view_tasks()
#             update_task()
#         elif choice == "8":
#             view_tasks()
#         elif choice == "9":
#             view_tasks()
#             mark_task_complete()
#         elif choice == "10":
#             view_tasks()
#             delete_task()
#         elif choice == "0":
#             print("Goodbye!")
#             break
#         else:
#             print("Invalid option. Please choose a valid number.")

# def add_lesson():
#     while True:
#         title = input("Enter lesson title: ")
#         if title.strip():
#             break
#         else:
#             print("Title cannot be empty. Please enter a valid title.")
    
#     while True:
#         date = input("Enter lesson date (YYYY-MM-DD): ")
#         if validate_date(date):
#             break
#         else:
#             print("Invalid date format. Please use YYYY-MM-DD.")
    
#     while True:
#         time = input("Enter lesson time (HH:MM): ")
#         if validate_time(time):
#             break
#         else:
#             print("Invalid time format. Please use HH:MM.")
    
#     while True:
#         subject = input("Enter lesson subject: ")
#         if subject.strip():
#             break
#         else:
#             print("Subject cannot be empty. Please enter a valid subject.")
    
#     while True:
#         try:
#             default_students = int(input("Enter default number of students: "))
#             if default_students >= 0:
#                 break
#             else:
#                 print("Number of students cannot be negative. Please enter a valid number.")
#         except ValueError:
#             print("Invalid input. Please enter a valid number.")
    
#     while True:
#         try:
#             session_price = float(input("Enter session price: "))
#             if session_price >= 0:
#                 break
#             else:
#                 print("Price cannot be negative. Please enter a valid price.")
#         except ValueError:
#             print("Invalid input. Please enter a valid price.")

#     notes = input("Enter lesson notes (optional): ")

#     connection = None  # Initialize connection variable here

#     try:
#         # Create the Lesson object
#         new_lesson = Lesson(title, date, time, subject, notes, default_students, session_price)

#         # Insert into the database
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute(''' 
#         INSERT INTO lessons (title, date, time, subject, notes, completed, default_students, session_price)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#         ''', (title, date, time, subject, notes, 0, default_students, session_price))
#         connection.commit()

#         print(f"Lesson '{new_lesson.title}' added successfully!")

#     except sqlite3.OperationalError as e:
#         print(f"Database error occurred: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#     finally:
#         if connection:  # Only close if connection was initialized
#             connection.close()
# def update_lesson():
#     while True:
#         lesson_id = input("Enter the ID of the lesson to update: ")
#         if validate_id(lesson_id):
#             break
#         else:
#             print("Invalid ID. Please enter a positive integer.")
    
#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute('SELECT * FROM lessons WHERE id = ?', (lesson_id,))
#         lesson = cursor.fetchone()

#         if lesson:
#             print("\n--- Current Lesson Details ---")
#             print(f"Title: {lesson[1]}, Date: {lesson[2]}, Time: {lesson[3]}, Subject: {lesson[4]}, Notes: {lesson[5]}, Default Students: {lesson[6]}, Session Price: {lesson[7]}")

#             while True:
#                 new_title = input(f"Enter new title (Leave blank to keep '{lesson[1]}'): ") or lesson[1]
#                 if new_title.strip():
#                     break
#                 else:
#                     print("Title cannot be empty. Please enter a valid title.")

#             while True:
#                 new_date = input(f"Enter new date (Leave blank to keep '{lesson[2]}', use YYYY-MM-DD): ") or lesson[2]
#                 if validate_date(new_date):
#                     break
#                 else:
#                     print("Invalid date format. Please use YYYY-MM-DD.")
            
#             while True:
#                 new_time = input(f"Enter new time (Leave blank to keep '{lesson[3]}', use HH:MM): ") or lesson[3]
#                 if validate_time(new_time):
#                     break
#                 else:
#                     print("Invalid time format. Please use HH:MM.")

#             while True:
#                 new_subject = input(f"Enter new subject (Leave blank to keep '{lesson[4]}'): ") or lesson[4]
#                 if new_subject.strip():
#                     break
#                 else:
#                     print("Subject cannot be empty. Please enter a valid subject.")

#             new_notes = input(f"Enter new notes (Leave blank to keep '{lesson[5]}'): ") or lesson[5]

#             while True:
#                 try:
#                     new_default_students = input(f"Enter new default number of students (Leave blank to keep '{lesson[6]}'): ") or lesson[6]
#                     if new_default_students.strip() == "":
#                         new_default_students = lesson[6]
#                     else:
#                         new_default_students = int(new_default_students)
#                     if new_default_students >= 0:
#                         break
#                     else:
#                         print("Number of students cannot be negative. Please enter a valid number.")
#                 except ValueError:
#                     print("Invalid input. Please enter a valid number.")
            
#             while True:
#                 try:
#                     new_session_price = input(f"Enter new session price (Leave blank to keep '{lesson[7]}'): ") or lesson[7]
#                     if new_session_price.strip() == "":
#                         new_session_price = lesson[7]
#                     else:
#                         new_session_price = float(new_session_price)
#                     if new_session_price >= 0:
#                         break
#                     else:
#                         print("Price cannot be negative. Please enter a valid price.")
#                 except ValueError:
#                     print("Invalid input. Please enter a valid price.")

#             cursor.execute(''' 
#                 UPDATE lessons
#                 SET title = ?, date = ?, time = ?, subject = ?, notes = ?, default_students = ?, session_price = ?
#                 WHERE id = ?
#             ''', (new_title, new_date, new_time, new_subject, new_notes, new_default_students, new_session_price, lesson_id))

#             connection.commit()
#             print(f"Lesson with ID {lesson_id} updated successfully!")
#         else:
#             print(f"No lesson found with ID {lesson_id}.")
    
#     except sqlite3.OperationalError as e:
#         print(f"Database error occurred: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#     finally:
#         connection.close()


# def delete_lesson():
#     while True:
#         lesson_id = input("Enter the ID of the lesson to delete: ")
#         if validate_id(lesson_id):
#             break
#         else:
#             print("Invalid ID. Please enter a positive integer.")
    
#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute('SELECT * FROM lessons WHERE id = ?', (lesson_id,))
#         lesson = cursor.fetchone()

#         if lesson:
#             confirmation = input(f"Are you sure you want to delete the lesson '{lesson[1]}'? (y/n): ").lower()
#             if confirmation == 'y':
#                 cursor.execute('DELETE FROM lessons WHERE id = ?', (lesson_id,))
#                 connection.commit()
#                 print(f"Lesson with ID {lesson_id} deleted successfully!")
#             else:
#                 print("Lesson deletion canceled.")
#         else:
#             print(f"No lesson found with ID {lesson_id}.")
    
#     except sqlite3.OperationalError as e:
#         print(f"Database error occurred: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#     finally:
#         connection.close()

# def view_lessons():
#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM lessons")
#         lessons = cursor.fetchall()

#         if lessons:
#             print("\n--- All Lessons ---")
#             for lesson in lessons:
#                 status = "Completed" if lesson[6] == 1 else "Incomplete"  # lesson[6] is the 'completed' field
#                 print(f"ID: {lesson[0]}, Title: {lesson[1]}, Date: {lesson[2]}, Time: {lesson[3]}, "
#                       f"Subject: {lesson[4]}, Notes: {lesson[5]}, Default Students: {lesson[7]}, "
#                       f"Session Price: ${lesson[8]:.2f}, Status: {status}")
#         else:
#             print("No lessons found.")

#     except sqlite3.OperationalError as e:
#         print(f"Database error occurred: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#     finally:
#         connection.close()

# def mark_lesson_complete():
#     while True:
#         lesson_id = input("Enter the ID of the lesson to mark as complete: ")
#         if validate_id(lesson_id):
#             break
#         else:
#             print("Invalid ID. Please enter a positive integer.")

#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute('SELECT id FROM lessons WHERE id = ?', (lesson_id,))
#         result = cursor.fetchone()

#         if result:
#             cursor.execute('UPDATE lessons SET completed = 1 WHERE id = ?', (lesson_id,))
#             connection.commit()
#             print(f"Lesson with ID {lesson_id} marked as completed.")
#         else:
#             print(f"Lesson with ID {lesson_id} does not exist.")

#     except sqlite3.OperationalError as e:
#         print(f"Database error occurred: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#     finally:
#         connection.close()

# def add_task():
#     while True:
#         description = input("Enter task description: ")
#         if description.strip():
#             break
#         else:
#             print("Description cannot be empty. Please enter a valid task description.")
    
#     while True:
#         due_date = input("Enter due date (YYYY-MM-DD): ")
#         if validate_date(due_date):
#             break
#         else:
#             print("Invalid date format. Please use YYYY-MM-DD.")

#     try:
#         new_task = Task(description, due_date)

#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute("INSERT INTO tasks (description, due_date, status) VALUES (?, ?, ?)",
#                        (new_task.description, new_task.due_date, new_task.status))
#         connection.commit()

#         print(f"Task '{new_task.description}' added successfully!")

#     except sqlite3.OperationalError as e:
#         print(f"Database error occurred: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#     finally:
#         connection.close()

# def update_task():
#     while True:
#         task_id = input("Enter the ID of the task to update: ")
#         if validate_id(task_id):
#             break
#         else:
#             print("Invalid ID. Please enter a positive integer.")

#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
#         task = cursor.fetchone()

#         if task:
#             print("\n--- Current Task Details ---")
#             print(f"Description: {task[1]}, Due Date: {task[2]}, Status: {'Complete' if task[3] else 'Incomplete'}")
            
#             while True:
#                 new_description = input(f"Enter new description (Leave blank to keep '{task[1]}'): ") or task[1]
#                 if new_description.strip():
#                     break
#                 else:
#                     print("Description cannot be empty. Please enter a valid description.")

#             while True:
#                 new_due_date = input(f"Enter new due date (Leave blank to keep '{task[2]}', use YYYY-MM-DD): ") or task[2]
#                 if validate_date(new_due_date):
#                     break
#                 else:
#                     print("Invalid due date format. Please use YYYY-MM-DD.")

#             cursor.execute('''
#                 UPDATE tasks
#                 SET description = ?, due_date = ?
#                 WHERE id = ?
#             ''', (new_description, new_due_date, task_id))

#             connection.commit()
#             print(f"Task with ID {task_id} updated successfully!")
#         else:
#             print(f"No task found with ID {task_id}.")
    
#     except sqlite3.OperationalError as e:
#         print(f"Database error occurred: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#     finally:
#         connection.close()

# def delete_task():
#     while True:
#         task_id = input("Enter the ID of the task to delete: ")
#         if validate_id(task_id):
#             break
#         else:
#             print("Invalid ID. Please enter a positive integer.")
    
#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
#         task = cursor.fetchone()

#         if task:
#             confirmation = input(f"Are you sure you want to delete the task '{task[1]}'? (y/n): ").lower()
#             if confirmation == 'y':
#                 cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
#                 connection.commit()
#                 print(f"Task with ID {task_id} deleted successfully!")
#             else:
#                 print("Task deletion canceled.")
#         else:
#             print(f"No task found with ID {task_id}.")
    
#     except sqlite3.OperationalError as e:
#         print(f"Database error occurred: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#     finally:
#         connection.close()

# def view_tasks():
#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM tasks")
#         tasks = cursor.fetchall()

#         if tasks:
#             print("\n--- All Tasks ---")
#             for task in tasks:
#                 print(f"ID: {task[0]}, Description: {task[1]}, Due Date: {task[2]}, Status: {'Complete' if task[3] else 'Incomplete'}")
#         else:
#             print("No tasks found.")

#     except sqlite3.OperationalError as e:
#         print(f"Database error occurred: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#     finally:
#         connection.close()

# def mark_task_complete():
#     while True:
#         task_id = input("Enter the ID of the task to mark as complete: ")
#         if validate_id(task_id):
#             break
#         else:
#             print("Invalid ID. Please enter a positive integer.")

#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute('SELECT id FROM tasks WHERE id = ?', (task_id,))
#         result = cursor.fetchone()

#         if result:
#             cursor.execute('UPDATE tasks SET status = 1 WHERE id = ?', (task_id,))
#             connection.commit()
#             print(f"Task with ID {task_id} marked as completed.")
#         else:
#             print(f"Task with ID {task_id} does not exist.")

#     except sqlite3.OperationalError as e:
#         print(f"Database error occurred: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#     finally:
#         connection.close()


# db_init()
# menu()


# main.py

# main.py

from tkinter import Tk
from gui.interface import LessonPlannerApp 
from db.db_init import init_db, add_columns_if_not_exists
import sqlite3

def db_init():
    connection = sqlite3.connect('db/planner.db')
    cursor = connection.cursor()
    init_db()
    add_columns_if_not_exists(cursor)
    connection.commit()
    connection.close()

if __name__ == "__main__":
    db_init()  # Initialize the database
    root = Tk()  # Create the main window
    app = LessonPlannerApp(root)  # Instantiate the LessonPlannerApp
    root.mainloop()  # Start the GUI event loop
