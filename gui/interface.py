import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import sqlite3

# Function to validate day of the week
def validate_day(day_str):
    valid_days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    return day_str in valid_days

def validate_time(time_str):
    try:
        datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False

def validate_id(input_str):
    return input_str.isdigit()

def get_db_connection():
    return sqlite3.connect('db/planner.db')


class LessonPlannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lesson Planner")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")

        # Frame setup: split into left and right halves
        left_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        right_frame = tk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Buttons for adding/updating lessons
        tk.Button(left_frame, text="Add Lesson", command=self.add_lesson).pack(pady=5)
        tk.Button(left_frame, text="Update Lesson", command=self.update_lesson).pack(pady=5)
        tk.Button(left_frame, text="Incomplete/Completed", command=self.mark_lesson_complete).pack(pady=5)
        tk.Button(left_frame, text="Delete Lesson", command=self.delete_lesson).pack(pady=5)
        
        # Adding space before the entries
        tk.Label(left_frame).pack(pady=(10, 0))  # Empty label to create space
        
        self.title_entry = self.create_form_entry(left_frame, "Title")
        self.date_entry = self.create_form_entry(left_frame, "Day of the Week (e.g. Monday)")
        self.time_entry = self.create_form_entry(left_frame, "Time (HH:MM)")
        self.subject_entry = self.create_form_entry(left_frame, "Subject")
        self.default_students_entry = self.create_form_entry(left_frame, "Default Students")
        self.session_price_entry = self.create_form_entry(left_frame, "Session Price")
        self.notes_entry = self.create_form_text(left_frame, "Notes (optional)")  # Use create_form_text for the notes field

        # Create a Treeview for displaying lessons
        self.lesson_list = ttk.Treeview(right_frame, columns=("ID", "Title", "Day of Week", "Time", "Subject", "Notes", "Completed", "Default Students", "Session Price"), show="headings")

        # Create vertical scrollbar
        self.yscrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.lesson_list.yview)
        self.lesson_list.configure(yscrollcommand=self.yscrollbar.set)

        # Create horizontal scrollbar
        self.xscrollbar = ttk.Scrollbar(right_frame, orient="horizontal", command=self.lesson_list.xview)
        self.lesson_list.configure(xscrollcommand=self.xscrollbar.set)

        # Define column headings and widths
        self.lesson_list.heading("ID", text="ID")
        self.lesson_list.heading("Title", text="Title")
        self.lesson_list.heading("Day of Week", text="Day of Week")
        self.lesson_list.heading("Time", text="Time")
        self.lesson_list.heading("Subject", text="Subject")
        self.lesson_list.heading("Notes", text="Notes")
        self.lesson_list.heading("Completed", text="Completed")
        self.lesson_list.heading("Default Students", text="Students")
        self.lesson_list.heading("Session Price", text="Price")

        # Set column widths (adjust as necessary)
        self.lesson_list.column("ID", width=10)
        self.lesson_list.column("Title", width=150)
        self.lesson_list.column("Day of Week", width=70)
        self.lesson_list.column("Time", width=50)
        self.lesson_list.column("Subject", width=50)
        self.lesson_list.column("Notes", width=150)
        self.lesson_list.column("Completed", width=50)
        self.lesson_list.column("Default Students", width=20)
        self.lesson_list.column("Session Price", width=50)

        # Pack the Treeview and scrollbars
        self.lesson_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Load existing lessons
        self.load_lessons()
        self.lesson_list.bind("<<TreeviewSelect>>", lambda event: self.populate_entries())




    def create_form_entry(self, parent, label_text):
        tk.Label(parent, text=label_text).pack()
        
        if label_text == "Day of the Week (e.g. Monday)":
            # Combo box for days of the week
            days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            entry = ttk.Combobox(parent, values=days_of_week, state="readonly")
            entry.set("Select Day")
            entry.pack()

        elif label_text == "Time (HH:MM)":
            # Create combo boxes for hours and minutes in 24-hour format
            hour_label = tk.Label(parent, text="Hour:")
            hour_label.pack()
            hours = [str(h).zfill(2) for h in range(24)]  # Hours from 00 to 23
            hour_combo = ttk.Combobox(parent, values=hours, state="readonly")
            hour_combo.set("Select Hour")
            hour_combo.pack()

            minute_label = tk.Label(parent, text="Minute:")
            minute_label.pack()
            minutes = [str(m).zfill(2) for m in range(60)]  # Minutes from 00 to 59
            minute_combo = ttk.Combobox(parent, values=minutes, state="readonly")
            minute_combo.set("Select Minute")
            minute_combo.pack()

            entry = (hour_combo, minute_combo)  # Return a tuple of both combo boxesbo, period_combo)  # Return a tuple of all three combo boxes

            
        else:
            # Default to a regular entry for other labels
            entry = tk.Entry(parent)
            entry.pack()

        return entry



    def create_form_text(self, parent, label_text, height=5, width=30):
        label = tk.Label(parent, text=label_text)
        label.pack()
        text_widget = tk.Text(parent, height=height, width=width)
        text_widget.pack()
        return text_widget

    def load_lessons(self):
        # Clear any existing rows in the lesson list
        for row in self.lesson_list.get_children():
            self.lesson_list.delete(row)
        
        # Connect to the database and retrieve all columns from the lessons table
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM lessons")
        lessons = cursor.fetchall()
        connection.close()
        
        # Insert each lesson into the lesson list
        for lesson in lessons:
            # Check completed status (assumed to be the seventh column)
            status = "Completed" if lesson[6] else "Incomplete"
            # Include all columns, ensure to place status correctly
            self.lesson_list.insert("", "end", values=(lesson[0], lesson[1], lesson[2], lesson[3], lesson[4], lesson[5], status, lesson[7], lesson[8]))

    def add_lesson(self):
        title = self.title_entry.get()
        day_of_week = self.date_entry.get()
        hour_combo, minute_combo = self.time_entry
        hour = hour_combo.get()
        minute = minute_combo.get()
        time = f"{hour}:{minute}"  # Format as HH:MM
        subject = self.subject_entry.get()
        notes = self.notes_entry.get("1.0", "end-1c")
        
        try:
            default_students = int(self.default_students_entry.get())
            session_price = float(self.session_price_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for Default Students and Session Price.")
            return

        if not (title and validate_day(day_of_week) and validate_time(time) and subject):
            messagebox.showerror("Error", "Please fill in all fields with valid data.")
            return

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO lessons (title, day_of_week, time, subject, notes, completed, default_students, session_price) 
                          VALUES (?, ?, ?, ?, ?, 0, ?, ?)''', 
                          (title, day_of_week, time, subject, notes, default_students, session_price))
        connection.commit()
        connection.close()

        messagebox.showinfo("Success", f"Lesson '{title}' added successfully!")
        self.load_lessons()

    def update_lesson(self):
        selected_item = self.lesson_list.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a lesson to update.")
            return

        lesson_id = self.lesson_list.item(selected_item)["values"][0]
        title = self.title_entry.get()
        day_of_week = self.date_entry.get()    
        hour_combo, minute_combo = self.time_entry
        hour = hour_combo.get()
        minute = minute_combo.get()
        time = f"{hour}:{minute}"  # Format as HH:MM
        subject = self.subject_entry.get()
        notes = self.notes_entry.get("1.0", "end-1c")
        
        try:
            default_students = int(self.default_students_entry.get())
            session_price = float(self.session_price_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for Default Students and Session Price.")
            return

        if not (title and validate_day(day_of_week) and validate_time(time) and subject):
            messagebox.showerror("Error", "Please fill in all fields with valid data.")
            return

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''UPDATE lessons SET title=?, day_of_week=?, time=?, subject=?, notes=?, default_students=?, session_price=? 
                          WHERE id=?''', 
                          (title, day_of_week, time, subject, notes, default_students, session_price, lesson_id))
        connection.commit()
        connection.close()

        messagebox.showinfo("Success", f"Lesson '{title}' updated successfully!")
        self.load_lessons()

    def mark_lesson_complete(self):
        selected_item = self.lesson_list.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a lesson to toggle completion status.")
            return

        lesson_id = self.lesson_list.item(selected_item)["values"][0]

        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Get the current completed status of the lesson
        cursor.execute("SELECT completed FROM lessons WHERE id=?", (lesson_id,))
        current_status = cursor.fetchone()[0]

        # Toggle the completion status
        new_status = 0 if current_status == 1 else 1
        cursor.execute("UPDATE lessons SET completed=? WHERE id=?", (new_status, lesson_id))

        # Commit changes and close the connection
        connection.commit()
        connection.close()

        # Show a success message and reload the lessons
        status_text = "completed" if new_status == 1 else "incomplete"
        messagebox.showinfo("Success", f"Lesson marked as {status_text}!")
        self.load_lessons()


    def delete_lesson(self):
        selected_item = self.lesson_list.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a lesson to delete.")
            return

        lesson_id = self.lesson_list.item(selected_item)["values"][0]

        # Confirmation prompt
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this lesson?")
        if confirm:  # If the user clicks "Yes"
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute('''DELETE FROM lessons WHERE id=?''', (lesson_id,))
            connection.commit()
            connection.close()

            messagebox.showinfo("Success", "Lesson deleted successfully!")
            self.load_lessons()

    def populate_entries(self):
        selected_item = self.lesson_list.focus()
        if not selected_item:
            return
        
        lesson_id = self.lesson_list.item(selected_item)["values"][0]
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT title, day_of_week, time, subject, notes, default_students, session_price FROM lessons WHERE id=?", (lesson_id,))
        record = cursor.fetchone()
        connection.close()
        
        if record:
            title, day_of_week, time, subject, notes, default_students, session_price = record
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, title)
            self.date_entry.set(day_of_week)
            
            # Split time into hour and minute for combo boxes
            hour, minute = time.split(":")
            hour_combo, minute_combo = self.time_entry
            hour_combo.set(hour)
            minute_combo.set(minute)
            
            self.subject_entry.delete(0, tk.END)
            self.subject_entry.insert(0, subject)
            
            self.notes_entry.delete("1.0", tk.END)
            self.notes_entry.insert("1.0", notes)
            
            self.default_students_entry.delete(0, tk.END)
            self.default_students_entry.insert(0, str(default_students))
            
            self.session_price_entry.delete(0, tk.END)
            self.session_price_entry.insert(0, str(session_price))

if __name__ == "__main__":
    root = tk.Tk()
    app = LessonPlannerGUI(root)
    root.mainloop()
