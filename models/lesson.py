class Lesson:
    def __init__(self, title, date, time, subject, notes='', completed=False):
        self.title = title
        self.date = date
        self.time = time
        self.subject = subject
        self.notes = notes
        self.completed = completed

    def mark_completed(self):
        self.completed = True

    def edit_lesson(self, title=None, date=None, time=None, subject=None, notes=None):
        if title: self.title = title
        if date: self.date = date
        if time: self.time = time
        if subject: self.subject = subject
        if notes: self.notes = notes
