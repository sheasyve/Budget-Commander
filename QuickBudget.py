#Quickbudget Budget Manager
#Written by Shea Syverson 

import sys
import re

class expense:
    def __init__(self,name, cost, description = ""):
        self.name = name
        self.cost = cost
        self.description = description

def remove_expense(expenses,name):
    for i,e in enumerate(expenses):
        if e.name == name:
            del expenses[i]
            return expenses

def expense_prompt(name,cost,costin,saved_expenses,managing):
    name = input("Enter the name of the expense\n")
    saved_expense = esearch_e(saved_expenses,name)
    if saved_expense != None:
        return saved_expense
    costin = input("Enter the cost of the expense\n")
    while re.match(r"\d",costin) == None:
        costin = input("Cost must be a number\n")
    cost = float(costin)
    description = input("Enter a description or leave it blank\n")
    command = ""
    if managing == False:
        command = input("Enter s to save the expense for reuse or enter to continue\n")
    if command == "s" or command == "S" or managing:
        saved_expences = remove_expense(saved_expenses,name)
        if description == "":
            saved_expenses.append(expense(name,cost,name))
            save_expenses(saved_expenses)
        else:
            saved_expenses.append(expense(name,cost,description))
            save_expenses(saved_expenses)
    if description == "":
        return expense(name,cost,name)
    else:
        return expense(name,cost,description)

def display_budget(expenses, funds):
    remaining_funds = funds
    print("\nStarting budget: " + str(funds))
    for e in expenses:
        new_funds = remaining_funds - e.cost
        print(e.name + ": " + str(remaining_funds) + " - " + str(e.cost) + " = " + str(new_funds))
        remaining_funds = new_funds
    print("Total remaining funds: " + str(remaining_funds) + "\n")

def list_expenses(expenses):
    print("Expenses:")
    for e in expenses:
        print(e.name)

def esearch_e(expenses,name):
    for e in expenses:
        if re.fullmatch(e.name,name, re.IGNORECASE):
            return e
    return None

def esearch(expenses):
    ename = input("Enter the name of the expense to modify or 0 to go back\n")
    if ename == "0":
        return "-1"
    expense = esearch_e(expenses, ename)
    while expense == None:
        ename = input("Expense not found, enter an expense or 0 to go back\n")
        if ename == "0":
            return "-1"
        expense = esearch_e(expenses, ename)
    return expense

def modify_expense(expenses):
    expense = esearch(expenses)
    command = "0"
    if expense != "-1":
        command = input("Commands:\n1 - Modify the name, 2 - to modify the cost, 3 - Modify description, 0 - Go back\n")
    while re.match(r"1||2||3||0",command) == None:
        print("Incorrect command")
        command = input("Commands:\n1 - Modify the name, 2 - to modify the cost, 3 - Modify description, 0 - Go back\n")
    if command == "1":
        new_name = input("Enter the new name\n")
        expense.name = new_name
        print("The name has been updated")
    elif command == "2":
        costin = input("Enter the new cost\n")
        while re.match(r"\d",costin) == None:
            costin = input("Cost must be a number\n")
        expense.cost = float(costin)
        print("The cost has been updated")
    elif command == "3":
        new_desc = input("Enter the new description\n")
        expense.description = new_desc
        print("The description has been updated")

def make_budget(saved_expenses):
    f = input("Enter your funds\n")
    while re.match(r"\d",f) == None:
        f = input("Funds must be a number\n")
    funds = float(f)
    expenses = []
    manage_budget(funds,expenses,saved_expenses)

def manage_budget(funds,expenses,saved_expenses):
    command = input("Commands:\n1 - Add an expense, 2 - View the current budget, 3 - List saved expenses,\n4 - Modify budget expense, 5 - Modify saved expense, 0 - Go back\n")
    while command != "0":
        if command == "1":
            name,description,cost = "","",0
            expenses.append(expense_prompt(name,cost,description,saved_expenses,False))
        elif command == "2":
            display_budget(expenses,funds)
        elif command == "3":
            list_saved_expenses(saved_expenses)
        elif command == "4":
            list_expenses(expenses)
            modify_expense(expenses)
        elif command == "5":
            list_expenses(saved_expenses)
            modify_expense(saved_expenses)
            save_expenses(saved_expenses)
        else:
            print("You have entered an incorrect command")
        command = input("Commands:\n1 - Add an expense, 2 - View the current budget, 3 - List saved expenses,\n4 - Modify budget expense, 5 - Modify saved expense, 0 - Go back\n")

def save_expenses(expenses):
    f = open('expenses.txt', 'w', encoding="utf-8")
    for e in expenses:
        f.write("n\n"+ e.name +"\nc\n" + str(e.cost) + "\nd\n" + e.description + "\n")
    f.close()

def load_expenses():
    expenses = []
    f = open('expenses.txt', 'r', encoding="utf-8")
    n,c,d = "",0,""
    line = f.readline()
    while len(line) != 0:
        if re.match(r"n",line):
            line = f.readline()
            n = line.strip()
            f.readline()
            line = f.readline()
            c = float(line.strip())
            f.readline()
            line = f.readline()
            d = line.strip()
            expenses.append(expense(n,c,d))
        line = f.readline()
    return expenses

def clear_expenses(saved_expenses):
    saved_expenses = []
    f = open('expenses.txt', 'w', encoding="utf-8")
    f.close()

def manage_saved_expenses(saved_expenses):
    command = input("Commands: 1 - Add an expense, 2 - Modify expense, 3 - List expenses, 4 - Clear saved expenses, 0 - Go back\n")
    while command != "0":
        if command == "1":
            name,description,cost = "","",0
            e = expense_prompt(name,cost,description,saved_expenses,True)
            saved_expenses.append(e)
        elif command == "2":
            modify_expense(saved_expenses)
            save_expenses(saved_expenses)
        elif command == "3":
            list_saved_expenses(saved_expenses)
        elif command == "4":
            clear_expenses(saved_expenses)
            print("Expenses cleared")
        else:
            print("Incorrect command entered")
        command = input("Commands: 1 - Add an expense, 2 - Modify expense, 3 - List expenses, 4 - Clear saved expenses, 0 - Go back\n")

def list_saved_expenses(saved_expenses):
    for e in saved_expenses:
        print("Name: " + e.name)
        print("Cost: " + str(e.cost))
        print("Description: " + e.description + "\n")

def main():
    print("Welcome to QuickBudget")
    userin = input("Enter 1 to make a new budget, 2 to manage saved expenses, or 0 to quit.\n")
    saved_expenses = load_expenses()
    while(userin != "0"):
        if(userin == "1"):
            make_budget(saved_expenses)
        elif userin == "2":
            manage_saved_expenses(saved_expenses)
            saved_expenses = load_expenses()
        else:
            print("You have entered an incorrect command")
        userin = input("Commands:\n1 - Make a new budget, 2 - Manage saved expenses, 0 - Quit.\n")
    print("Goodbye")

if __name__ == "__main__":
    main()
