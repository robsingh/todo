from datetime import date
from datetime import datetime

task_list = []

def add_task():
    task_name = input("Enter the task details: ")
    task_list.append(task_name)
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    today_day = now.strftime("%A")
    print(f"Task '{task_name}' added to the list on '{today_day}' at {date_time}.")


def list_task():
      if not task_list:
        print("No tasks currently!")
      else:
        print("Current tasks: ")
        for index, task in enumerate(task_list, start=1):
            print(f"Task {index} -> {task}")

    
def delete_task():
    list_task()
    try:
        taskToDelete = int(input("Enter the task # to delete: "))
        index = taskToDelete - 1 # because user sees tasks starting from 1
        if 0 <= index < len(task_list):
            removed_task = task_list.pop(index)
            print(f"Task '{removed_task}' has been removed.")
        else:
            print(f"Task #{taskToDelete} was not found! Please try again with correct input.")
    except ValueError:
        print("Invalid Input! Please enter a number.")
    


if __name__ == "__main__":
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
            print("4. Quit!")
            print()

            choice = input("Enter your choice: ") # use int(input()) later

            if (choice == "1"):
                add_task()
            elif (choice == "2"):
                delete_task()
            elif (choice == "3"):
                list_task()
            elif (choice == "4"):
                break
            else:
                print("Invalid Input! Please enter an integer!")