from datetime import date
from datetime import datetime
import sqlite3

task_list = []
deleted_tasks = []

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


def list_task():
      if not task_list:
        print("No tasks currently!")
      else:
        print("Current tasks: ")
        sorted_tasks = sorted(task_list, key=lambda x:x['priority'])
        for index, task in enumerate(sorted_tasks, start=1):
            status = "✅ Done" if task["completed"] else "⌛️ Pending"
            print(f"{index}. {task['name']} | Priority: {task['priority']} | Status: {status} | Added on: {task['created_at']}")


def mark_task_completed():
    list_task()
    if not task_list:
        return "No tasks to mark."
    try:
        task_num = int(input("Enter the task # to mark as completed: "))
        index = task_num - 1
        if 0 <= index < len(task_list):
            if task_list[index]["completed"]:
                print(f"Task '{task_list[index]['name']}' is already marked as completed.")
            else:
                task_list[index]["completed"] = True
                print(f"Task '{task_list[index]['name']}' is marked as completed.")
        else:
            print(f"Invalid task number.")
    except ValueError:
        print(f"Invalid Input. Please enter a valid number.")

    
def delete_task():
    list_task()
    if not task_list:
        return None
    try:
        taskToDelete = int(input("Enter the task # to delete: "))
        index = taskToDelete - 1 # because user sees tasks starting from 1
        if 0 <= index < len(task_list):
            removed_task = task_list.pop(index)
            removed_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            removed_task["removed_at"] = removed_at
            deleted_tasks.append(removed_task)
            print(f"Task '{removed_task['name']}' was removed at {removed_at}.")
        else:
            print(f"Task #{taskToDelete} was not found! Please try again with correct input.")
    except ValueError:
        print("Invalid Input! Please enter a number.")
    

def view_deleted_tasks():
    if not deleted_tasks:
        return None
    else:
        print("Deleted Tasks: ")
        for index, task in enumerate(deleted_tasks, start=1):
            print(f"{task['name']} | Added on: {task['created_at']} | Removed at: {task['removed_at']} ")


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
            for index, row in enumerate(records, start=1):
                task_id, name, created_at, priority, completed = row
                status = "✅ Done" if completed else "⌛️ Pending"
                print(f"{index}. {name} | Priority: {priority} | Status: {status} | Added on: {created_at}")

    except sqlite3.OperationalError as e:
            print(f"Oops! Error: {e}")



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
                delete_task()
            elif (choice == "3"):
                list_task()
            elif (choice == "4"):
                mark_task_completed()
            elif (choice == "5"):
                view_deleted_tasks()
            elif (choice == "6"):
                break
            else:
                print("Invalid Input! Please enter an integer!")
            