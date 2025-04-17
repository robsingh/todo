#procedural code to Object-Oriented design

from datetime import datetime
import sqlite3

class Task:
    def __init__(self, id, name, created_at, priority, completed=False, removed_at=None):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.priority = priority
        self.completed = bool(completed)
        self.removed_at = removed_at

    def mark_completed(self):
        self.completed = True

    def mark_deleted(self):
        self.removed_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    def __str__(self):
        status = "✅ Done" if self.completed else "⌛️ Pending"
        return f"{self.id:<4} {self.name:<30} {self.priority:<8} {status:<10} {self.created_at}"
    

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.deleted_tasks = []

    def load_from_db(self):
        '''
        load active tasks from db
        convert each record into a Task object
        append them to self.tasks
        '''
        try:
            with sqlite3.connect('todo.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                SELECT id, name, created_at, priority, completed
                FROM tasks
                WHERE removed_at IS NULL
                ''')
                records = cursor.fetchall()
                if not records:
                    print(f"No active records found!")
                    return
                
                for row in records:
                    task_id, name, created_at, priority, completed = row
                    task = Task(task_id, name, created_at, priority, completed)
                    self.tasks.append(task)
            
        except sqlite3.OperationalError as e:
            print(f"Database Error: {e}")

    def add_task(self,name,priority):
        pass

    def delete_task(self, id):
        pass

    def mark_task_completed(self, id):
        pass

    def list_tasks(self):
        pass

    def view_deleted_tasks(self):
        pass

    
