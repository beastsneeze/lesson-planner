class Lesson:
    def __init__(self, title, date, time, subject, notes='', default_students=0, session_price=0.0, completed=False):
        self.title = title
        self.date = date
        self.time = time
        self.subject = subject
        self.notes = notes
        self.default_students = default_students
        self.session_price = session_price
        self.completed = completed

    def mark_completed(self):
        self.completed = True

    def edit_lesson(self, title=None, date=None, time=None, subject=None, notes=None, default_students=None, session_price=None):
        if title is not None: self.title = title
        if date is not None: self.date = date
        if time is not None: self.time = time
        if subject is not None: self.subject = subject
        if notes is not None: self.notes = notes
        if default_students is not None: self.default_students = default_students
        if session_price is not None: self.session_price = session_price