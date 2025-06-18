import json
from datetime import datetime

tasksList = []

with open("tasks.json", "r") as tasks:
    data = json.load(tasks)

    tasksList = data['Tasks']

def validate(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False

def printError(message):
    print("--------------")
    print("ERROR: "+message)
    print("--------------")

def ViewTasks():
    print("------------")
    print("Tasks list")
    print("------------")
    for task in tasksList:
        print(str(task['id']) + ": " + task['description'])
        print("Due: " + task['due_date'])
        print("----------------")
    menu()

def AddTask():
    print("--------------------")
    print("Enter a description (Type 'C' to cancel)")
    print("--------------------")
    desc = input()
    if desc != "C":
        print("-----------------------------")
        print("Enter a due date (YYYY-MM-DD)")
        print("-----------------------------")
        dDate = input()
        try:
            if validate(dDate):
                newData = {"id": len(tasksList)+1,"description": desc, "due_date": dDate, "completed": False}
                write_Json(newData)
        except ValueError:
            printError("Error with date")
        
    menu()

def write_Json(new_data, filename="tasks.json"):
    try:
        with open(filename,'r+') as file:
            file_data = json.load(file)
            file_data["Tasks"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent=4)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        printError("Error reading or writing JSON file: " + e)    


def menu():
    print("------------")
    print("Tasks Menu")
    print("-------------")
    print("1: View Tasks")
    print("2: Add Task")
    print("3: Complete Task")
    print("4: Remove Task")
    print("5: Exit")
    print("---------------")
    while True:
        inputSel = input()
        if inputSel == "1":
            ViewTasks()
        elif inputSel == "2":
            AddTask()


menu()