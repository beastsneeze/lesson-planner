from tkinter import *
from tkinter import messagebox
from models.lesson import Lesson
import sqlite3
from datetime import datetime
from db.db_init import init_db, add_columns_if_not_exists

def get_db_connection():
    return sqlite3.connect('db/planner.db')

def db_init():
    connection = sqlite3.connect('db/planner.db')
    cursor = connection.cursor()
    init_db()
    add_columns_if_not_exists(cursor)
    connection.commit()
    connection.close()

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_time(time_str):
    try:
        datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False

def validate_id(input_str):
    return input_str.isdigit()

class LessonPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lesson Planner")

        # Lesson fields
        self.title_var = StringVar()
        self.date_var = StringVar()
        self.time_var = StringVar()
        self.subject_var = StringVar()
        self.notes_var = StringVar()
        self.default_students_var = IntVar()
        self.session_price_var = DoubleVar()

        self.create_widgets()

    def create_widgets(self):
        Label(self.root, text="Title").grid(row=0, column=0)
        Entry(self.root, textvariable=self.title_var).grid(row=0, column=1)

        Label(self.root, text="Date (YYYY-MM-DD)").grid(row=1, column=0)
        Entry(self.root, textvariable=self.date_var).grid(row=1, column=1)

        Label(self.root, text="Time (HH:MM)").grid(row=2, column=0)
        Entry(self.root, textvariable=self.time_var).grid(row=2, column=1)

        Label(self.root, text="Subject").grid(row=3, column=0)
        Entry(self.root, textvariable=self.subject_var).grid(row=3, column=1)

        Label(self.root, text="Notes").grid(row=4, column=0)
        Entry(self.root, textvariable=self.notes_var).grid(row=4, column=1)

        Label(self.root, text="Default Students").grid(row=5, column=0)
        Entry(self.root, textvariable=self.default_students_var).grid(row=5, column=1)

        Label(self.root, text="Session Price").grid(row=6, column=0)
        Entry(self.root, textvariable=self.session_price_var).grid(row=6, column=1)

        Button(self.root, text="Add Lesson", command=self.add_lesson).grid(row=7, column=0, columnspan=2)

        Button(self.root, text="View Lessons", command=self.view_lessons).grid(row=8, column=0, columnspan=2)

        Button(self.root, text="Update Lesson", command=self.update_lesson).grid(row=9, column=0, columnspan=2)

        Button(self.root, text="Delete Lesson", command=self.delete_lesson).grid(row=10, column=0, columnspan=2)

    def add_lesson(self):
        title = self.title_var.get()
        date = self.date_var.get()
        time = self.time_var.get()
        subject = self.subject_var.get()
        notes = self.notes_var.get()
        default_students = self.default_students_var.get()
        session_price = self.session_price_var.get()

        if not all([title, date, time, subject]) or default_students < 0 or session_price < 0:
            messagebox.showerror("Input Error", "Please fill in all fields correctly.")
            return

        if not validate_date(date) or not validate_time(time):
            messagebox.showerror("Input Error", "Please provide valid date and time formats.")
            return

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(''' 
                INSERT INTO lessons (title, date, time, subject, notes, completed, default_students, session_price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (title, date, time, subject, notes, 0, default_students, session_price))
            connection.commit()
            messagebox.showinfo("Success", f"Lesson '{title}' added successfully!")
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            connection.close()

    def view_lessons(self):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM lessons")
            lessons = cursor.fetchall()

            lesson_list = ""
            for lesson in lessons:
                status = "Completed" if lesson[6] == 1 else "Incomplete"
                lesson_list += f"ID: {lesson[0]}, Title: {lesson[1]}, Date: {lesson[2]}, Time: {lesson[3]}, Subject: {lesson[4]}, Notes: {lesson[5]}, Default Students: {lesson[7]}, Session Price: ${lesson[8]:.2f}, Status: {status}\n"

            if lesson_list:
                messagebox.showinfo("All Lessons", lesson_list)
            else:
                messagebox.showinfo("All Lessons", "No lessons found.")
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            connection.close()

    def update_lesson(self):
        lesson_id = simpledialog.askinteger("Update Lesson", "Enter Lesson ID to update:")
        if lesson_id is None or not validate_id(str(lesson_id)):
            messagebox.showerror("Input Error", "Please enter a valid Lesson ID.")
            return
        
        # Fetch the lesson to update
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM lessons WHERE id = ?', (lesson_id,))
            lesson = cursor.fetchone()

            if lesson:
                self.title_var.set(lesson[1])
                self.date_var.set(lesson[2])
                self.time_var.set(lesson[3])
                self.subject_var.set(lesson[4])
                self.notes_var.set(lesson[5])
                self.default_students_var.set(lesson[7])
                self.session_price_var.set(lesson[8])
                
                self.add_lesson()
            else:
                messagebox.showerror("Update Error", f"No lesson found with ID {lesson_id}.")
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            connection.close()

    def delete_lesson(self):
        lesson_id = simpledialog.askinteger("Delete Lesson", "Enter Lesson ID to delete:")
        if lesson_id is None or not validate_id(str(lesson_id)):
            messagebox.showerror("Input Error", "Please enter a valid Lesson ID.")
            return

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM lessons WHERE id = ?', (lesson_id,))
            lesson = cursor.fetchone()

            if lesson:
                confirmation = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the lesson '{lesson[1]}'?")
                if confirmation:
                    cursor.execute('DELETE FROM lessons WHERE id = ?', (lesson_id,))
                    connection.commit()
                    messagebox.showinfo("Success", f"Lesson with ID {lesson_id} deleted successfully!")
            else:
                messagebox.showerror("Delete Error", f"No lesson found with ID {lesson_id}.")
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            connection.close()

if __name__ == "__main__":
    db_init()
    root = Tk()
    app = LessonPlannerApp(root)
    root.mainloop()
