class Task:
    def __init__(self, description, due_date, status=False):
        self.description = description
        self.due_date = due_date
        self.status = status

    def mark_complete(self):
        self.status = True

    def edit_task(self, description=None, due_date=None):
        if description: self.description = description
        if due_date: self.due_date = due_date
