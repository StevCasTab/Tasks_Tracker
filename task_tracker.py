import json
from datetime import datetime


#-----------------------------------------
#Main Variables
#-----------------------------------------

#Loaded Tasks List
tasksList = []

#Directory to JSON file
myJsonFile = "tasks.json"

#-----------------------------------------




#-----------------------------------------
#Initialization
#-----------------------------------------
with open(myJsonFile, "r") as tasks:
    data = json.load(tasks) #Load File
    tasksList = data['Tasks'] #Retrieve Tasks Array
#-----------------------------------------



#--------------------------------------------------------------------------------------------------------
#Functions
#--------------------------------------------------------------------------------------------------------

#Validate string as date
def validate(date_text):
    try:
        #Check if date text is a valid date
        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            #If not, trigger a Value Error
            raise ValueError
        return True
    except ValueError:
        #Print Error Message
        printError("Inputted date was incorrect. Please make sure to enter date in YYYY-MM-DD format")
        return False

#Print Error Message
def printError(message):
    print("--------------")
    print("ERROR: " + message)
    print("--------------")

#Print Tasks List
def ViewTasks():
    print("------------")
    print("Tasks list")
    print("----------------")
    for task in tasksList:
        printTask(task)
    menu()

#Print specific Task
def printTask(task):
    print(str(task['id']) + ": " + task['description'])
    print("Due: " + task['due_date'])
    if(task['completed']):
        print("Completed: Yes")
    else:
        print("Completed: No")
    print("----------------")

#Add a Task
def AddTask():
    print("--------------------")
    print("Enter a description (Type 'C' to cancel)")
    print("--------------------")
    
    #User Enters a description for the new task
    desc = input() 

    #if the user did not enter the character 'C' only, proceed
    if desc != "C":
        print("-----------------------------")
        print("Enter a due date (YYYY-MM-DD) (Type 'C' to cancel)")
        print("-----------------------------")

        #User Enters a due date for the new task
        dDate = input()

        #if the user did not enter the character 'C' only, proceed
        if dDate != 'C':
            #Attempt to validate the entered date
            if validate(dDate):

                #Retrieve the current max integer of the 'id' attribute
                max_id = max((task["id"] for task in tasksList), default=0)

                #Calculate new Id
                new_id = max_id+1

                #Create new JSON data
                newData = {"id": new_id,"description": desc, "due_date": dDate, "completed": False}

                #Call function to write new data
                write_Json(newData, "Write")
        
    menu()

#Function to Write, Update, or Delete JSON
def write_Json(mode, new_data = None, task = None):
    global tasksList #Retrieve current global tasks list

    try:
        with open(myJsonFile,'r+') as file:
            #Load Json File
            file_data = json.load(file)

            #If the mode is set as a 'Write' operation
            if mode == 'Write':

                #Add the new json data to the json array
                file_data["Tasks"].append(new_data)

                #Return to beginning of JSON file
                file.seek(0)

                #Write updated content to the JSON file
                json.dump(file_data, file, indent=4)

            #If the mode is set as either an 'Update' or 'Delete operation
            elif mode == "Update" or mode == "Delete":
                #Return to beginning of JSON file
                file.seek(0)

                #If the mode is set as a 'Delete' operation
                if mode == "Delete":
                    #Remove the specified task from the current tasks list
                    tasksList.remove(task)
                
                #Create brand new JSON from scratch after modifications
                updatedJson = {"Tasks": tasksList}

                #Write updated content to the JSON file
                json.dump(updatedJson, file, indent=4)

            #If the mode is not a 'Delete' operation
            if mode != "Delete":
                #Retrieve updated JSON data and update the tasks list
                tasksList = file_data["Tasks"]

            #Resize file to reflect JSON array size
            file.truncate()

    #If JSON was unable to be decoded or the file was not found
    except (json.JSONDecodeError, FileNotFoundError) as e:
        #Return Error
        printError("Error attempting " + mode + " operation on JSON file: " + e)    

#Set task status to completed
def CompleteTask():
    print("------------------------------------------")
    print("Please enter task ID (Type 'C' to cancel)")
    print("------------------------------------------")

    #User enters task ID
    task_id = input()

    #If user has not entered the character 'C' alone, proceed
    if task_id != 'C':

        for task in tasksList:
            #Find the specific task that contains the matching task id
            if str(task["id"]) == task_id:

                #If the task was already set as completed
                if(task["completed"]):
                   
                   #Inform user that the task has already been completed
                   print("-------------------------")
                   print("Task " + task_id + " is already completed")
                   print("-------------------------")


                else:
                    print("----------------------")
                    printTask(task)
                    print("Are you sure? (Y/N) (Type 'C' to cancel)")

                    #Ask user for confirmation to mark task as completed
                    yesNo = input()

                    #If user has not entered the character 'C' alone and the user confirms the action, proceed
                    if yesNo != 'C' and yesNo == 'Y':
                            task['completed'] = True
                            write_Json("Update", None, None)
    menu()


#Remove a task from list
def RemoveTask():
    print("------------------------------------------")
    print("Please enter task ID (Type 'C' to cancel)")
    print("------------------------------------------")

    #User enters a task ID
    task_id = input()

    #If user has not entered the character 'C' alone, proceed
    if task_id != 'C':

        for task in tasksList:
            #Find the specific task that contains the matching task id
            if str(task["id"]) == task_id:
                print("----------------------")
                printTask(task)
                print("Are you sure you want to delete? (Y/N) (Type 'C' to cancel)")

                #Ask the user for confirmation
                yesNo = input()

                #If the user has not entered the character 'C' alone and confirms the action, proceed
                if yesNo != "C" and yesNo == "Y":
                    write_Json("Delete", None, task)

    menu()
#--------------------------------------------------------------------------------------------------------



#-----------------------------------------
#Main Program
#-----------------------------------------
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
        printError("Entered Option is invalid. Please enter a valid option (1-5)")
        menu()


menu()
#-----------------------------------------