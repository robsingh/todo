# To-Do App
### Purpose of the Application

It is a basic To-Do application. A good practical example of CRUD processes. A very beginner friendly project to solidify your knowledge of fundamentals. The main purpose of this application is to create a task, delete a task and view the list of the tasks. More features will be added soon! 

### Language Requirements
Python 3.x

### Scope of Improvement? (WIP)

- Store the list in the memory so that it can be viewed after quitting the program. 
    * SQLite database.
        * A cursor in SQLite is an object that allows you to execute SQL queries and fetch results. Basically a middleware between SQLite database connection and SQL query. It is created after giving connection to SQLite database.

- View the date and time when an item was added and removed. 
    * Added the functionality to view when was a task is added.
    * Added the functionality to capture the timestamp when a task is deleted and keep a record of deleted tasks (recycle bin).

- Add the priority order of a task in the list. For example, 1 defines most important and 5 defines least important.
    * Added the functionality to add the priority order of the task.

- Mark a task as completed.

- Sort Tasks by Priority before Displaying.
 