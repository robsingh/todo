from datetime import date
from datetime import datetime
import sqlite3

def add_task():
    task_name = input("Enter the task details: ")
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    
    #input validation for priority
    while True:
        try:
            task_priority = int(input("Enter task's priority (1-5): "))
            if 1 <= task_priority <= 5:
                break
            else:
                print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid Input. Please enter a valid number.")

    add_task_to_db(task_name, date_time, task_priority)
    
    print(f"Task '{task_name}' added to the list on {date_time}.")


def setup_database():
    try:
        with sqlite3.connect('todo.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tasks(
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT NOT NULL,
                           created_at TEXT NOT NULL,
                           priority INTEGER NOT NULL,
                           completed INTEGER DEFAULT 0,
                           removed_at TEXT)
            ''')
            conn.commit()

    except sqlite3.OperationalError as e:
        print(f"Failed to open database: {e}")


def add_task_to_db(name, created_at, priority):
    try:
        with sqlite3.connect('todo.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                        INSERT INTO tasks(name,created_at,priority)
                        VALUES(?,?,?)''',
                        (name, created_at, priority))
            conn.commit()

    except sqlite3.OperationalError as e:
        print(f"Failed to connect with the database: {e}")


def list_tasks_from_db():
    try:
        with sqlite3.connect('todo.db') as conn:
            cursor = conn.cursor()
            #get all tasks that have not been deleted
            cursor.execute('''
                    SELECT id, name, created_at, priority, completed
                    FROM tasks where removed_at IS NULL
            ''')
            records = cursor.fetchall()
            if not records:
                print(f"No active tasks found.")
                return
            
            print("Current Tasks:")
            print(f"{'ID':<4} {'Task':<30} {'Priority':<8} {'Status':<10} {'Created At'}")
            print("-" * 70)
            
            for row in records:
                task_id, name, created_at, priority, completed = row
                status = "✅ Done" if completed else "⌛️ Pending"
                print(f"{task_id}:<4 {name:<30} {priority:<8} {status:<10} {created_at}")

    except sqlite3.OperationalError as e:
            print(f"Oops! Error: {e}")


def mark_task_completed_in_db():
    list_tasks_from_db()
    try:
        task_id = int(input("Enter the task ID to mark as completed: "))
        with sqlite3.connect('todo.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                        UPDATE tasks
                        SET completed = 1
                        where id = ? AND removed_at IS NULL
                        ''', (task_id,))
            conn.commit()

            if cursor.rowcount == 0:
                print("❌ No active task found with that ID.")
            else:
                print("✅ Task marked as completed.")
    except ValueError:
        print("⚠️ Invalid Input! Please enter a valid task ID.")
    except sqlite3.OperationalError as e:
        print(f"Database Error: {e}")


def delete_task_from_db():
    list_tasks_from_db()
    try:
        task_id = int(input("Enter the task ID to delete: "))
        removed_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        with sqlite3.connect('todo.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE tasks
                SET removed_at = ?
                where id = ? AND removed_at IS NULL
                ''', (removed_at, task_id))
            conn.commit()

            if cursor.rowcount == 0:
                print("❌ No active tasks found with that ID.")
            else:
                print(f"🗑️ Task ID {task_id} marked as deleted at {removed_at}.")
    
    except ValueError:
        print("⚠️ Invalid Input! Please enter a valid task ID.")
    except sqlite3.OperationalError as e:
        print(f"Database Error: {e}")


def view_deleted_tasks_from_db():
    list_tasks_from_db()
    try:
        with sqlite3.connect('todo.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT id, name, created_at, removed_at
            FROM tasks
            WHERE removed_at IS NULL
            ORDER BY removed_at DESC
        ''')
            deleted = cursor.fetchall()
            if not deleted:
                print("🧼 No deleted tasks found!")
            else:
                print(f"{'ID':<4} {'Task':<30} {'Created At':<20} {'Removed At'}")
    
    except sqlite3.OperationalError as e:
        print(f"Database Error: {e}")


if __name__ == "__main__":
        setup_database()
        print("Welcome to the To-Do list app, a very introductory app!")
        while True:
            print("\n")
            print("Please select one of the following options:")
            print()
            print("1. Add a new Task")
            print()
            print("2. Delete a Task")
            print()
            print("3. List Tasks")
            print()
            print("4. Mark a task as Completed")
            print()
            print("5. View Deleted Tasks")
            print()
            print("6. Quit!")
            print()

            choice = input("Enter your choice: ") # use int(input()) later

            if (choice == "1"):
                add_task()
            elif (choice == "2"):
                delete_task_from_db()
            elif (choice == "3"):
                list_tasks_from_db()
            elif (choice == "4"):
                mark_task_completed_in_db()
            elif (choice == "5"):
                view_deleted_tasks_from_db()
            elif (choice == "6"):
                break
            else:
                print("Invalid Input! Please enter an integer!")
            