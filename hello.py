import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import re

# File to store expenses
EXPENSE_FILE = 'expenses.txt'

# Function to load expenses from file
def load_expenses():
    if not os.path.exists(EXPENSE_FILE):
        return []
    with open(EXPENSE_FILE, 'r') as file:
        return [line.strip() for line in file]

# Function to save expense to file
def save_expense(expense):
    with open(EXPENSE_FILE, 'a') as file:
        file.write(expense + '\n')

# Function to clear all expenses from file
def clear_expenses():
    open(EXPENSE_FILE, 'w').close()

# Function to extract numbers from a string and sum them up
def extract_numbers(text):
    numbers = re.findall(r'[\d.]+', text)
    return sum(float(num) for num in numbers)

# Function to calculate total expenses
def calculate_total():
    total = 0
    expenses = load_expenses()
    for expense in expenses:
        total += extract_numbers(expense)
    return total

# Function to update the expense list and total
def update_expense_list():
    listbox_expenses.delete(0, tk.END)
    for expense in load_expenses():
        listbox_expenses.insert(tk.END, expense)
    update_total_label()

# Function to update total label
def update_total_label():
    total = calculate_total()
    label_total.config(text=f"Total Expenses: ${total:.2f}")

# Function to add expense
def add_expense():
    expense = entry_expense.get()
    if expense:
        save_expense(expense)
        update_expense_list()
        entry_expense.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter an expense.")

# Function to refresh the tracker
def refresh_tracker():
    clear_expenses()
    update_expense_list()
    update_total_label()

# Create the main window
root = tk.Tk()
root.title("Personal Expense Tracker")

# Load images
try:
    img = Image.open("icon.png")
    img = img.resize((50, 50), Image.ANTIALIAS)
    icon = ImageTk.PhotoImage(img)
    root.iconphoto(False, icon)
except FileNotFoundError:
    pass  # No icon available

# Create and place widgets
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Enter Expense:").grid(row=0, column=0, padx=5, pady=5)

entry_expense = tk.Entry(frame, width=30)
entry_expense.grid(row=0, column=1, padx=5, pady=5)

btn_add = tk.Button(frame, text="Add Expense", command=add_expense)
btn_add.grid(row=0, column=2, padx=5, pady=5)

btn_refresh = tk.Button(frame, text="Refresh", command=refresh_tracker)
btn_refresh.grid(row=0, column=3, padx=5, pady=5)

listbox_expenses = tk.Listbox(frame, width=50, height=10)
listbox_expenses.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

label_total = tk.Label(frame, text="Total: $0.00")
label_total.grid(row=2, column=0, columnspan=4, pady=5)

update_expense_list()

# Start the main loop
root.mainloop()
