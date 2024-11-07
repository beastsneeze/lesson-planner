import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import sqlite3

# Function to validate day of the week
def validate_day(day_str):
    valid_days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    return day_str in valid_days

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
        self.start_time_entry = self.create_form_entry(left_frame, "Start Time (HH:MM)")
        self.end_time_entry = self.create_form_entry(left_frame, "End Time (HH:MM)")
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

        elif label_text in ["Start Time (HH:MM)", "End Time (HH:MM)"]:
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
            # Check completed status (assumed to be the seventh column)
            status = "Completed" if lesson[6] else "Incomplete"
            # Include all columns, ensure to place status correctly
            self.lesson_list.insert("", "end", values=(lesson[0], lesson[1], lesson[2], lesson[3], lesson[9], lesson[4], lesson[5], status, lesson[7], lesson[8]))

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

        # Convert 12-hour time to 24-hour time for database storage
        try:
            s_time_24h = datetime.strptime(s_time_12h, '%I:%M %p').strftime('%H:%M')
            e_time_24h = datetime.strptime(e_time_12h, '%I:%M %p').strftime('%H:%M')
        except ValueError:
            messagebox.showerror("Error", "Please select valid start and end times.")
            return

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
                        (title, day_of_week, s_time_24h, subject, notes, default_students, session_price, e_time_24h))
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

        # Convert 12-hour time to 24-hour time for database storage
        try:
            s_time_24h = datetime.strptime(s_time_12h, '%I:%M %p').strftime('%H:%M')
            e_time_24h = datetime.strptime(e_time_12h, '%I:%M %p').strftime('%H:%M')
        except ValueError:
            messagebox.showerror("Error", "Please select valid start and end times.")
            return

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
        cursor.execute('''UPDATE lessons SET title=?, day_of_week=?, start_time=?, subject=?, notes=?, default_students=?, session_price=?, end_time=? 
                        WHERE id=?''', 
                        (title, day_of_week, s_time_24h, subject, notes, default_students, session_price, e_time_24h, lesson_id))
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

        # Retrieve lesson details and unpack
        lesson = self.lesson_list.item(selected_item, "values")
        lesson_id, title, day_of_week, start_time, end_time, subject, notes, completed, default_students, session_price = lesson

        # Set entry fields based on retrieved lesson
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, title)
        self.date_entry.set(day_of_week)

        # Parse and set start time
        try:
            s_hour, s_minute, s_period = datetime.strptime(start_time, '%H:%M').strftime('%I %M %p').split()
            self.start_time_entry[0].set(s_hour)
            self.start_time_entry[1].set(s_minute)
            self.start_time_entry[2].set(s_period)
        except ValueError:
            messagebox.showerror("Error", "Invalid start time format in database.")

        # Parse and set end time
        try:
            e_hour, e_minute, e_period = datetime.strptime(end_time, '%H:%M').strftime('%I %M %p').split()
            self.end_time_entry[0].set(e_hour)
            self.end_time_entry[1].set(e_minute)
            self.end_time_entry[2].set(e_period)
        except ValueError:
            messagebox.showerror("Error", "Invalid end time format in database.")

        self.subject_entry.delete(0, tk.END)
        self.subject_entry.insert(0, subject)
        self.notes_entry.delete("1.0", tk.END)
        self.notes_entry.insert("1.0", notes)

        # Handle non-string values like integers and floats separately
        self.default_students_entry.delete(0, tk.END)
        self.default_students_entry.insert(0, str(default_students))
        self.session_price_entry.delete(0, tk.END)
        self.session_price_entry.insert(0, str(session_price))

if __name__ == "__main__":
    root = tk.Tk()
    app = LessonPlannerGUI(root)
    root.mainloop()
