import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient
from bson import ObjectId

# ------------------- MongoDB Connection -------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["collegedata"]
collection = db["students"]

# ------------------- Functions -------------------
def create_record():
    roll = entry_roll.get()
    name = entry_name.get()
    age = entry_age.get()
    course = entry_course.get()
    city = entry_city.get()

    if roll and name and age and course and city:
        collection.insert_one({
            "roll": roll,
            "name": name,
            "age": int(age),
            "course": course,
            "city": city
        })
        messagebox.showinfo("Success", "Record inserted successfully")
        clear_entries()
        read_records()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

def read_records():
    listbox.delete(0, tk.END)
    for doc in collection.find():
        listbox.insert(
            tk.END,
            f"{doc['_id']} | Roll: {doc['roll']} | {doc['name']} | {doc['age']} | {doc['course']} | {doc['city']}"
        )

def update_record():
    selected = listbox.get(tk.ACTIVE)
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a record")
        return

    record_id = selected.split(" | ")[0]

    roll = entry_roll.get()
    name = entry_name.get()
    age = entry_age.get()
    course = entry_course.get()
    city = entry_city.get()

    if roll and name and age and course and city:
        collection.update_one(
            {"_id": ObjectId(record_id)},
            {"$set": {
                "roll": roll,
                "name": name,
                "age": int(age),
                "course": course,
                "city": city
            }}
        )
        messagebox.showinfo("Success", "Record updated successfully")
        clear_entries()
        read_records()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

def delete_record():
    selected = listbox.get(tk.ACTIVE)
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a record")
        return

    record_id = selected.split(" | ")[0]
    collection.delete_one({"_id": ObjectId(record_id)})
    messagebox.showinfo("Success", "Record deleted successfully")
    read_records()

def search_records():
    keyword = entry_search.get()
    listbox.delete(0, tk.END)

    if keyword:
        query = {
            "$or": [
                {"roll": {"$regex": keyword, "$options": "i"}},
                {"name": {"$regex": keyword, "$options": "i"}},
                {"course": {"$regex": keyword, "$options": "i"}},
                {"city": {"$regex": keyword, "$options": "i"}}
            ]
        }
        results = collection.find(query)
        for doc in results:
            listbox.insert(
                tk.END,
                f"{doc['_id']} | Roll: {doc['roll']} | {doc['name']} | {doc['age']} | {doc['course']} | {doc['city']}"
            )
    else:
        read_records()

def clear_entries():
    entry_roll.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_course.delete(0, tk.END)
    entry_city.delete(0, tk.END)

# ------------------- GUI -------------------
root = tk.Tk()
root.title("MongoDB CRUD with Python GUI (Roll No + Search)")

# Input Fields
tk.Label(root, text="Roll No:").grid(row=0, column=0, padx=5, pady=5)
entry_roll = tk.Entry(root)
entry_roll.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Name:").grid(row=1, column=0, padx=5, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Age:").grid(row=2, column=0, padx=5, pady=5)
entry_age = tk.Entry(root)
entry_age.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Course:").grid(row=3, column=0, padx=5, pady=5)
entry_course = tk.Entry(root)
entry_course.grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="City:").grid(row=4, column=0, padx=5, pady=5)
entry_city = tk.Entry(root)
entry_city.grid(row=4, column=1, padx=5, pady=5)

# Buttons
tk.Button(root, text="Create", command=create_record).grid(row=5, column=0, padx=5, pady=5)
tk.Button(root, text="Read", command=read_records).grid(row=5, column=1, padx=5, pady=5)
tk.Button(root, text="Update", command=update_record).grid(row=6, column=0, padx=5, pady=5)
tk.Button(root, text="Delete", command=delete_record).grid(row=6, column=1, padx=5, pady=5)

# Search Section
tk.Label(root, text="Search:").grid(row=7, column=0, padx=5, pady=5)
entry_search = tk.Entry(root)
entry_search.grid(row=7, column=1, padx=5, pady=5)
tk.Button(root, text="Search", command=search_records).grid(row=7, column=2, padx=5, pady=5)

# Listbox
listbox = tk.Listbox(root, width=110)
listbox.grid(row=8, column=0, columnspan=3, padx=5, pady=10)

read_records()  # Load records on startup
root.mainloop()
