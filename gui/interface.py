import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import Toplevel
from datetime import datetime
import sqlite3

def silent_messagebox(title, message):
    root = Toplevel()
    root.title(title)
    root.geometry("300x100")
    
    label = tk.Label(root, text=message)
    label.pack(pady=20)
    
    ok_button = tk.Button(root, text="OK", command=root.destroy)
    ok_button.pack(pady=10)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f'+{x}+{y}')
    
    root.mainloop()
# background
bg = "light blue"
# Function to validate day of the week
def validate_time(hour, minute, period):
    """Validate time entries in 12-hour format (e.g., 01:15 PM)."""
    try:
        # Construct time string and validate using 12-hour format
        time_str = f"{hour}:{minute} {period}"
        parsed_time = datetime.strptime(time_str, '%I:%M %p')
        
        # Check for logical hour and minute ranges
        if parsed_time.hour < 1 or parsed_time.hour > 12 or parsed_time.minute < 0 or parsed_time.minute > 59:
            return False
        return True
    except ValueError:
        # If parsing fails, indicate invalid time
        return False

# Function to validate day of the week
def validate_day(day_str):
    valid_days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    return day_str in valid_days

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
        self.root.configure(bg=bg)

        # Frame setup: split into left and right halves
        left_frame = tk.Frame(root, bg=bg)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        right_frame = tk.Frame(self.root, bg=bg)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Buttons for adding/updating lessons
        tk.Button(left_frame, text="Add Lesson", command=self.add_lesson).pack(pady=5)
        tk.Button(left_frame, text="Update Lesson", command=self.update_lesson).pack(pady=5)
        tk.Button(left_frame, text="Incomplete/Completed", command=self.mark_lesson_complete).pack(pady=5)
        tk.Button(left_frame, text="Delete Lesson", command=self.delete_lesson).pack(pady=5)

        # Adding space before the entries
        tk.Label(left_frame, bg=bg).pack(pady=(10, 0))  # Empty label to create space

        self.title_entry = self.create_form_entry(left_frame, "Title")
        self.date_entry = self.create_form_entry(left_frame, "Day of the Week (e.g. Monday)")
        self.start_time_entry = self.create_form_entry(left_frame, "Start Time (HH:MM PR)")
        self.end_time_entry = self.create_form_entry(left_frame, "End Time (HH:MM PR)")
        self.subject_entry = self.create_form_entry(left_frame, "Subject")
        self.default_students_entry = self.create_form_entry(left_frame, "Default Students")
        self.session_price_entry = self.create_form_entry(left_frame, "Session Price")
        self.notes_entry = self.create_form_text(left_frame, "Notes (optional)")  # Use create_form_text for the notes field

        # Create a Treeview for displaying lessons
        self.lesson_list = ttk.Treeview(right_frame, columns=("ID", "Title", "Day of Week", "Start", "End", "Subject", "Notes", "Completed", "Default Students", "Session Price"), show="headings")

        # Create vertical scrollbar
        self.yscrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.lesson_list.yview)
        self.lesson_list.configure(yscrollcommand=self.yscrollbar.set)
        # Create horizontal scrollbar
        self.xscrollbar = ttk.Scrollbar(right_frame, orient="horizontal", command=self.lesson_list.xview)
        self.lesson_list.configure(xscrollcommand=self.xscrollbar.set)

        # Column setup
        columns_info = [
            ("ID", 10), ("Title", 150), ("Day of Week", 70), ("Start", 50), 
            ("End", 50), ("Subject", 50), ("Notes", 150), ("Completed", 50), 
            ("Default Students", 20), ("Session Price", 50)
        ]
        for col, width in columns_info:
            self.lesson_list.heading(col, text=col)
            self.lesson_list.column(col, width=width)

        # Pack the scrollbars first and Treeview last
        self.yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.lesson_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Load existing lessons
        self.load_lessons()
        self.lesson_list.bind("<<TreeviewSelect>>", lambda event: self.populate_entries())


    def create_form_entry(self, parent, label_text):
        tk.Label(parent, text=label_text, bg=bg).pack()

        if label_text == "Day of the Week (e.g. Monday)":
            # Combo box for days of the week
            days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            entry = ttk.Combobox(parent, values=days_of_week, state="readonly")
            entry.set("Select Day")
            entry.pack()

        elif label_text in ["Start Time (HH:MM PR)", "End Time (HH:MM PR)"]:
            # Create a frame to hold the hour, minute, and period comboboxes side by side
            time_frame = tk.Frame(parent)
            time_frame.pack()

            # Create combo boxes for hours, minutes, and period (AM/PM) in 12-hour format
            hour_combo = ttk.Combobox(time_frame, values=[str(h).zfill(2) for h in range(1, 13)], state="readonly", width=5)
            hour_combo.set("Hour")
            hour_combo.pack(side="left", padx=2)

            minute_combo = ttk.Combobox(time_frame, values=[str(m).zfill(2) for m in range(60)], state="readonly", width=5)
            minute_combo.set("Minute")
            minute_combo.pack(side="left", padx=2)

            period_combo = ttk.Combobox(time_frame, values=["AM", "PM"], state="readonly", width=5)
            period_combo.set("Period")
            period_combo.pack(side="left", padx=2)

            entry = (hour_combo, minute_combo, period_combo)  # Return a tuple of the combo boxes

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
            # Ensure the correct column indices
            lesson_id = lesson[0]  # ID
            title = lesson[1]  # Title
            day_of_week = lesson[2]  # Day of the week
            start_time = lesson[3]  # Start time
            end_time = lesson[4]  # End time (column 4)
            subject = lesson[5]  # Subject
            notes = lesson[6]  # Notes
            completed = lesson[7]  # Completed status (1 = Completed, 0 = Incomplete)
            default_students = lesson[8]  # Default number of students
            session_price = lesson[9]  # Session price

            # Check completed status
            status = "Completed" if completed else "Incomplete"

            # Insert values into the Treeview
            self.lesson_list.insert("", "end", values=(lesson_id, title, day_of_week, start_time, end_time, subject, notes, status, default_students, session_price))

    def add_lesson(self):
        title = self.title_entry.get()
        day_of_week = self.date_entry.get()
        s_hour_combo, s_minute_combo, s_period_combo = self.start_time_entry
        s_hour = s_hour_combo.get()
        s_minute = s_minute_combo.get()
        s_period = s_period_combo.get()
        s_time_12h = f"{s_hour}:{s_minute} {s_period}"

        e_hour_combo, e_minute_combo, e_period_combo = self.end_time_entry
        e_hour = e_hour_combo.get()
        e_minute = e_minute_combo.get()
        e_period = e_period_combo.get()
        e_time_12h = f"{e_hour}:{e_minute} {e_period}"

        subject = self.subject_entry.get()
        notes = self.notes_entry.get("1.0", "end-1c")

        try:
            default_students = int(self.default_students_entry.get())
            session_price = float(self.session_price_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for Default Students and Session Price.")
            return

        if not (title and validate_day(day_of_week) and subject):
            messagebox.showerror("Error", "Please fill in all fields with valid data.")
            return

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO lessons (title, day_of_week, start_time, subject, notes, completed, default_students, session_price, end_time) 
                    VALUES (?, ?, ?, ?, ?, 0, ?, ?, ?)''', 
                    (title, day_of_week, s_time_12h, subject, notes, default_students, session_price, e_time_12h))
        connection.commit()
        connection.close()

        silent_messagebox("Success", f"Lesson '{title}' added successfully!")
        self.load_lessons()


    def update_lesson(self):
        selected_item = self.lesson_list.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a lesson to update.")
            return

        lesson_id = self.lesson_list.item(selected_item)["values"][0]
        title = self.title_entry.get()
        day_of_week = self.date_entry.get()
        s_hour_combo, s_minute_combo, s_period_combo = self.start_time_entry
        s_hour = s_hour_combo.get()
        s_minute = s_minute_combo.get()
        s_period = s_period_combo.get()
        s_time_12h = f"{s_hour}:{s_minute} {s_period}"

        e_hour_combo, e_minute_combo, e_period_combo = self.end_time_entry
        e_hour = e_hour_combo.get()
        e_minute = e_minute_combo.get()
        e_period = e_period_combo.get()
        e_time_12h = f"{e_hour}:{e_minute} {e_period}"

        subject = self.subject_entry.get()
        notes = self.notes_entry.get("1.0", "end-1c")

        try:
            default_students = int(self.default_students_entry.get())
            session_price = float(self.session_price_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for Default Students and Session Price.")
            return

        if not (title and validate_day(day_of_week) and subject):
            messagebox.showerror("Error", "Please fill in all fields with valid data.")
            return

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''UPDATE lessons SET title=?, day_of_week=?, start_time=?, subject=?, notes=?, 
                    default_students=?, session_price=?, end_time=? WHERE id=?''', 
                    (title, day_of_week, s_time_12h, subject, notes, default_students, session_price, e_time_12h, lesson_id))
        connection.commit()
        connection.close()  

        silent_messagebox("Success", f"Lesson '{title}' updated successfully!")
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
        current_status = cursor.fetchone()

        # Toggle the completion status
        new_status = 0 if current_status == 1 else 1
        cursor.execute("UPDATE lessons SET completed=? WHERE id=?", (new_status, lesson_id))

        # Commit changes and close the connection
        connection.commit()
        connection.close()

        # Show a success message and reload the lessons
        status_text = "completed" if new_status == 1 else "incomplete"
        silent_messagebox("Success", f"Lesson marked as {status_text}!")
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

            silent_messagebox("Success", "Lesson deleted successfully!")
            self.load_lessons()



    def populate_entries(self):

        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM lessons"  # Modify this with your actual query to get the data
        cursor.execute(query)
        entries = cursor.fetchall()
        print(entries)
        for entry in entries:
            start_time = entry['start_time']  # Assume start_time is in 'HH:MM AM' format, adjust as needed
            
            # Check if start_time is in the valid format
            if start_time:
                try:
                    # Parse the time into hours, minutes, and period
                    time_parts = start_time.split()  # Split time and period (AM/PM)
                    time_values = time_parts[0].split(':')  # Split hours and minutes
                    hours = int(time_values[0])  # Hours as integer
                    minutes = int(time_values[1])  # Minutes as integer
                    period = time_parts[1] if len(time_parts) > 1 else 'AM'  # Get AM/PM or default to AM
                    
                    # Handle 12-hour format, convert to 24-hour format if needed
                    if period == 'PM' and hours < 12:
                        hours += 12
                    elif period == 'AM' and hours == 12:
                        hours = 0
                    
                    # Set the values to the combo boxes
                    self.hour_combo.setCurrentIndex(hours)
                    self.minute_combo.setCurrentIndex(minutes)
                    self.period_combo.setCurrentText(period)

                except ValueError:
                    print(f"Invalid start time format: {start_time}")
                    raise ValueError("Invalid start time format in database.")
            else:
                print("Start time is missing for an entry.")


if __name__ == "__main__":
    root = tk.Tk()
    root.bell(False)
    app = LessonPlannerGUI(root)
    root.mainloop()