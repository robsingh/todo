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
        self.setup_database() #ensures DB is ready when object is created


    def setup_database(self):
        '''
        creates the task table if it does not exist
        '''
        try:
            with sqlite3.connect('todo.db') as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS tasks(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    priority INTEGER NOT NULL,
                    completed INTEGER DEFAULT 0,
                    removed_at TEXT)'''
                )
                conn.commit()
        except sqlite3.OperationalError as e:
            print(f"Database Error: {e}")


    def add_task(self,name,priority):
        '''
        create a task object
        save it to db
        append it to self.tasks
        '''
        try:
            with sqlite3.connect('todo.db') as conn:
                cursor = conn.cursor()
                created_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                cursor.execute(
                '''
                INSERT INTO tasks(name,created_at,priority)
                VALUES (?,?,?)''',
                (name, created_at, priority))
                task_id = cursor.lastrowid
                task = Task(task_id,name,created_at, priority)
                self.tasks.append(task)

        except sqlite3.OperationalError as e:
            print(f"Failed to connect with the database: {e}")


    def load_from_db(self):
        self.tasks.clear()
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
            

    def list_tasks(self):
        if not self.tasks:
            print(f"No tasks loaded in memory.")
            return
        
        print(f"{'ID':<4} {'Task':<30} {'Priority':<8} {'Status':<10} {'Created At'}")
        print("-" * 70)
        for task in self.tasks:
            print(task)
        
    
    def mark_task_completed(self, id):
        try:
            with sqlite3.connect('todo.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                UPDATE tasks
                SET completed = 1
                where id = ? AND removed_at IS NULL
                ''', (id,))
                conn.commit()
                
                if cursor.rowcount == 0:
                    print(f"❌ No active tasks found with {id}.")
                else:
                    print(f"✅ {id} mark as completed.")
                
                for task in self.tasks:
                    if task.id == id:
                        task.mark_completed()
                        print(f"✅ Task marked as completed.")
                        print(task)

        except ValueError:
            print("Invalid Input! Please enter a valid task ID.")
        except sqlite3.OperationalError as e:
            print(f"Database Error: {e}")

    def delete_task(self, id):
        task_to_delete = None
        for task in self.tasks:
            if task.id == id:
                task.mark_deleted()
                task_to_delete = task
                break

        if not task_to_delete:
            print(f"❌ Task with ID {id} not found in memory.")
            return
        
        try:
            with sqlite3.connect('todo.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                               UPDATE tasks
                               SET removed_at = ?
                               WHERE id = ? AND removed_at IS NULL
                ''', (task_to_delete.removed_at, id))
                conn.commit()

                if cursor.rowcount == 0:
                    print(f"❌ No active tasks found with ID {id}.")
                else:
                    print(f"Task {id} is deleted.")

                    self.tasks.remove(task_to_delete)
                    self.deleted_tasks.append(task_to_delete)

        except ValueError:
            print("Invalid Input! Please enter a valid task ID.")
        except sqlite3.OperationalError as e:
            print(f"Database Error: {e}")


    def view_deleted_tasks(self):
        try:
            with sqlite3.connect('todo.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                        SELECT id, name, created_at, priority, completed, removed_at
                        FROM tasks 
                        WHERE removed_at IS NOT NULL
                        ORDER BY removed_at DESC
                        ''')
                deleted = cursor.fetchall()

                if not deleted:
                    print(f"No deleted tasks found!")
                    return
                
                print(f"{'ID':<4} {'Task':<30} {'Priority':<8} {'Status':<10} {'Created At':<20} {'Removed At'}")
                print("-" * 100)
                for row in deleted:
                    task_id, name, created_at, priority, completed, removed_at = row
                    task = Task(task_id, name, created_at, priority, completed, removed_at)
                    print(task)
                    self.deleted_tasks.append(task)

        except sqlite3.OperationalError as e:
            print(f"Database Error: {e}")

                

    
