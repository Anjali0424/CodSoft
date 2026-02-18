import tkinter as tk
from tkinter import messagebox
import json
import os

FILE_NAME = "contacts.json"


# -------------------------
# FILE FUNCTIONS
# -------------------------
def load_contacts():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as file:
        return json.load(file)


def save_contacts(contacts):
    with open(FILE_NAME, "w") as file:
        json.dump(contacts, file, indent=4)


# -------------------------
# CORE FUNCTIONS
# -------------------------
def refresh_list():
    listbox.delete(0, tk.END)
    contacts = load_contacts()

    for contact in contacts:
        listbox.insert(tk.END, f"{contact['name']} - {contact['phone']}")


def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()

    if not name or not phone:
        messagebox.showerror("Error", "Name and Phone required")
        return

    contacts = load_contacts()

    contacts.append({
        "name": name,
        "phone": phone,
        "email": email,
        "address": address
    })

    save_contacts(contacts)
    refresh_list()
    clear_fields()

    messagebox.showinfo("Success", "Contact added")


def delete_contact():
    selected = listbox.curselection()

    if not selected:
        messagebox.showerror("Error", "Select contact")
        return

    contacts = load_contacts()
    contacts.pop(selected[0])

    save_contacts(contacts)
    refresh_list()

    messagebox.showinfo("Success", "Contact deleted")


def search_contact():
    query = name_entry.get().lower()

    contacts = load_contacts()

    listbox.delete(0, tk.END)

    for contact in contacts:
        if query in contact["name"].lower() or query in contact["phone"]:
            listbox.insert(tk.END, f"{contact['name']} - {contact['phone']}")


def update_contact():
    selected = listbox.curselection()

    if not selected:
        messagebox.showerror("Error", "Select contact")
        return

    contacts = load_contacts()
    index = selected[0]

    contacts[index] = {
        "name": name_entry.get(),
        "phone": phone_entry.get(),
        "email": email_entry.get(),
        "address": address_entry.get()
    }

    save_contacts(contacts)
    refresh_list()

    messagebox.showinfo("Success", "Contact updated")


def fill_fields(event):
    selected = listbox.curselection()

    if not selected:
        return

    contacts = load_contacts()
    contact = contacts[selected[0]]

    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

    name_entry.insert(0, contact["name"])
    phone_entry.insert(0, contact["phone"])
    email_entry.insert(0, contact["email"])
    address_entry.insert(0, contact["address"])


def clear_fields():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)


# -------------------------
# GUI
# -------------------------
root = tk.Tk()
root.title("Contact Book")
root.geometry("500x500")
root.config(bg="#f0f0f0")


title = tk.Label(root, text="Contact Book", font=("Arial", 18, "bold"))
title.pack(pady=10)


# Input Fields
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Name").grid(row=0, column=0)
name_entry = tk.Entry(frame, width=30)
name_entry.grid(row=0, column=1)

tk.Label(frame, text="Phone").grid(row=1, column=0)
phone_entry = tk.Entry(frame, width=30)
phone_entry.grid(row=1, column=1)

tk.Label(frame, text="Email").grid(row=2, column=0)
email_entry = tk.Entry(frame, width=30)
email_entry.grid(row=2, column=1)

tk.Label(frame, text="Address").grid(row=3, column=0)
address_entry = tk.Entry(frame, width=30)
address_entry.grid(row=3, column=1)


# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add", width=10, command=add_contact).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Update", width=10, command=update_contact).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete", width=10, command=delete_contact).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Search", width=10, command=search_contact).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="Refresh", width=10, command=refresh_list).grid(row=0, column=4, padx=5)


# Listbox
listbox = tk.Listbox(root, width=60, height=15)
listbox.pack(pady=10)

listbox.bind("<<ListboxSelect>>", fill_fields)


# Load contacts initially
refresh_list()

root.mainloop()
