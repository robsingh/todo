task_list = []
def add_task():
    task_name = input("Enter the task details: ")
    task_list.append(task_name)
    print(f"Task '{task_name}' added to the list!")

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
        if taskToDelete >= 0 and taskToDelete < len(task_list):
            task_list.pop(taskToDelete)
            print(f"Task {taskToDelete} has been removed")
        else:
            print(f"Task #{taskToDelete} was not found! Please try again with correct input")
    except:
        print("Invalid Input!")
    




if __name__ == "__main__":
        print("Welcome to the To-Do list app, a very introductory app!")
        while True:
            print("\n")
            print("Please select one of the following options")
            print("\n")
            print("1. Add a new Task")
            print("2. Delete a Task")
            print("3. List Tasks")
            print("4. Quit!")

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