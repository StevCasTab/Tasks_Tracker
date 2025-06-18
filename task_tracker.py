import json
from datetime import datetime

tasksList = []
myJsonFile = "tasks.json"

with open(myJsonFile, "r") as tasks:
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
    print("----------------")
    for task in tasksList:
        printTask(task)
    menu()

def printTask(task):
    print(str(task['id']) + ": " + task['description'])
    print("Due: " + task['due_date'])
    if(task['completed']):
        print("Completed: Yes")
    else:
        print("Completed: No")
    print("----------------")

def AddTask():
    print("--------------------")
    print("Enter a description (Type 'C' to cancel)")
    print("--------------------")
    desc = input()
    if desc != "C":
        print("-----------------------------")
        print("Enter a due date (YYYY-MM-DD) (Type 'C' to cancel)")
        print("-----------------------------")
        dDate = input()
        if dDate != "C":
            try:
                if validate(dDate):
                    max_id = max((task["id"] for task in tasksList), default=0)
                    new_id = max_id+1
                    newData = {"id": new_id,"description": desc, "due_date": dDate, "completed": False}
                    write_Json(newData, "Write")
            except ValueError:
                printError("Error with date")
        
    menu()

def write_Json(mode, new_data = None, task = None):
    global tasksList
    comamndWord = mode
    try:
        with open(myJsonFile,'r+') as file:
            file_data = json.load(file)
            if mode == 'Write':
                comamndWord = "Writing"
                file_data["Tasks"].append(new_data)
                file.seek(0)
                json.dump(file_data, file, indent=4)
            elif mode == "Update" or mode == "Delete":
                file.seek(0)
                if mode == "Delete":
                    tasksList.remove(task)
                updatedJson = {"Tasks": tasksList}
                json.dump(updatedJson, file, indent=4)
                
            if mode != "Delete":
                tasksList = file_data["Tasks"]
            file.truncate()
    except (json.JSONDecodeError, FileNotFoundError) as e:
        printError("Error " + comamndWord + " JSON file: " + e)    


def CompleteTask():
    print("------------------------------------------")
    print("Please enter task ID (Type 'C' to cancel)")
    print("------------------------------------------")
    task_id = input()
    if task_id != "C":
        for task in tasksList:
            if str(task["id"]) == task_id:
                if(task["completed"]):
                   print("-------------------------")
                   print("Task " + task_id + " is already completed")
                   print("-------------------------")
                else:
                    print("----------------------")
                    printTask(task)
                    print("Are you sure? (Y/N) (Type 'C' to cancel)")
                    yesNo = input()
                    if yesNo != 'C':
                        if(yesNo == 'Y'):
                            task['completed'] = True
                            write_Json("Update", None, None)
    menu()

def RemoveTask():
    print("------------------------------------------")
    print("Please enter task ID (Type 'C' to cancel)")
    print("------------------------------------------")
    task_id = input()
    if task_id != "C":
        for task in tasksList:
            if str(task["id"]) == task_id:
                print("----------------------")
                printTask(task)
                print("Are you sure you want to delete? (Y/N) (Type 'C' to cancel)")
                yesNo = input()
                if yesNo != "C" and yesNo == "Y":
                    write_Json("Delete", None, task)

    menu()


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
   ##while True:
    inputSel = input()
    if inputSel == "1":
        ViewTasks()
    elif inputSel == "2":
        AddTask()
    elif inputSel == "3":
        CompleteTask()
    elif inputSel == "4":
        RemoveTask()
    else:
        menu()


menu()