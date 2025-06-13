#PERSONAL TASK MANAGER

import json
import getpass

#Function to load all registered users from file
def load_users():
    try:
        with open("users.txt", "r") as file:
            return json.load(file)
    except:
        return {}

#Function to save all users to file
def save_users(users):
    with open("users.txt", "w") as file:
        json.dump(users, file)

#Function to register a new user
def register():
    users = load_users()
    username = input("Enter a new username: ")
    if username in users:
        print("ERROR: This username is already taken. Please enter a new one")
        return None
    password = getpass.getpass("Enter a password: ")
    users[username] = password
    save_users(users)
    print("New user registered successfully!")
    return username

#Function to log in an existing user
def login():
    users = load_users()
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    if username in users and users[username] == password:
        print("Login successful!")
        return username
    else:
        print("ERROR: Incorrect username or password. Please try again!")
        return None

#Function to load the task list for a specific user
def load_tasks(username):
    try:
        with open("tasks.txt", "r") as file:
            all_tasks = json.load(file)
            return all_tasks.get(username, [])
    except:
        return []

#Function to save tasks for a specific user
def save_tasks(username, tasks):
    try:
        with open("tasks.txt", "r") as file:
            all_tasks = json.load(file)
    except:
        all_tasks = {}
    all_tasks[username] = tasks
    with open("tasks.txt", "w") as file:
        json.dump(all_tasks, file)

#Function to add a new task
def add_task(username):
    tasks = load_tasks(username)
    description = input("Enter the task description: ")
    tasks.append({"desc": description, "done": False})
    save_tasks(username, tasks)
    print("Task added successfully")

#Function to display all tasks for the user
def view_tasks(username):
    tasks = load_tasks(username)
    for index, task in enumerate(tasks, 1):
        status = "Done" if task["done"] else "Not Done"
        print(f"{index}. {task['desc']} - {status}")

#Function to mark selected tasks as done
def mark_done(username):
    tasks = load_tasks(username)
    view_tasks(username)
    try:
        index = int(input("Enter the number of the task to mark as done: ")) - 1
        if 0 <= index < len(tasks):
            tasks[index]["done"] = True
            save_tasks(username, tasks)
            print("Task marked as done")
        else:
            print("Invalid")
    except:
        print("ERROR: Task was not able to be marked as 'done'")

#Function to delete a particular task
def delete_task(username):
    tasks = load_tasks(username)
    view_tasks(username)
    try:
        index = int(input("Enter the number of the task to delete: ")) - 1
        tasks.pop(index)
        save_tasks(username, tasks)
        print("Task deleted successfully")
    except:
        print("ERROR: Task was not able to be deleted")

#Function to show task menu after logging in or registering
def task_menu(username):
    while True:
        print("\n1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Done")
        print("4. Delete Task")
        print("5. Logout")
        option = int(input("Please enter a number (acceptable values are 1, 2, 3, 4 & 5): "))
        if option == 1:
            add_task(username)
        elif option == 2:
            view_tasks(username)
        elif option == 3:
            mark_done(username)
        elif option == 4:
            delete_task(username)
        elif option == 5:
            break
        else:
            print("ERROR: Invalid option. Try again")

#Welcome message
print("Welcome to your Task Manager! What would you like to do today?")
while True:
    print("\n1. Sign Up")
    print("2. Log In")
    print("3. Exit")
    option = int(input("Please enter a number (acceptable values are 1, 2 & 3): "))
    if option == 1:
        user = register()
        if user:
            task_menu(user)
    elif option == 2:
        user = login()
        if user:
            task_menu(user)
    elif option == 3:
        print("Goodbye!")
        break
    else:
        print("ERROR: Invalid option")
