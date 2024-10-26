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

# db_init()
# menu()


import gui.interface 