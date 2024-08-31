from tkinter import *
from tkinter import messagebox
from random import *
import customtkinter as ctk
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
MY_EMAIL = "email@email.com"


def generate_password():
    nr_letters = randint(8, 10)
    nr_symbols = randint(2, 4)
    nr_numbers = randint(2, 4)

    password_letters = [choice(letters) for _ in range(nr_letters)]
    password_numbers = [choice(numbers) for _ in range(nr_numbers)]
    password_symbols = [choice(symbols) for _ in range(nr_symbols)]

    password_list = password_letters + password_numbers + password_symbols

    shuffle(password_list)

    password = "".join(password_list)

    password_input.delete(0, END)
    password_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def collect_data():
    website = website_input.get()
    email_address = email_input.get()
    created_password = password_input.get()
    new_data = {
        website: {
            "email": email_address,
            "password": created_password,
        }
    }

    if website == '' or email_address == '' or created_password == '':
        messagebox.showerror(title="Oops!", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except:
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_input.delete(0, END)
            password_input.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website_name = website_input.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found")
    if website_name in data:
        messagebox.showinfo(title=website_name,
                            message=f"Email: {data[website_name]["email"]}\nPassword: {data[website_name]["password"]}")
    else:
        messagebox.showerror(title="Error", message=f"No details for {website_name} exists.")


# ---------------------------- UI SETUP ------------------------------- #

# Set up window and canvas
window = ctk.CTk()
window.title("Password Manager")
window.config(padx=50, pady=50)
canvas = Canvas(width=200, height=200)

# Set up logo
logo_img = PhotoImage(file='Logo.png')
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Website Label
website_text = Label(text="Website:", font="bold")
website_text.grid(column=0, row=1)

# Website Fill in
website_input = ctk.CTkEntry(window, width=200, corner_radius=50)
website_input.grid(column=1, row=1, pady=3)
website_input.focus()

# Email Label
email_text = Label(text="Email/Username:", font="bold")
email_text.grid(column=0, row=2)

# Email Fill in
email_input = ctk.CTkEntry(window, width=200, corner_radius=50)
email_input.grid(column=0, row=2, columnspan=3, pady=3)
email_input.insert(0, MY_EMAIL)

# Password Label
password_text = Label(text="Password:", font="bold")
password_text.grid(column=0, row=3)

# Password Fill in
password_input = ctk.CTkEntry(window, width=200, corner_radius=50)
password_input.grid(column=1, row=3, pady=5)

# Password Button
pass_button = ctk.CTkButton(window, text="Generate Password", command=generate_password, border_width=2)
pass_button.grid(column=2, row=3, padx=10)

# Add Button
add_button = ctk.CTkButton(window, text="Add", width=200, command=collect_data, border_width=2)
add_button.grid(column=1, row=4)

# Search Button
search_button = ctk.CTkButton(window, text="Search", width=100, command=find_password, border_width=2)
search_button.grid(column=2, row=1)

window.mainloop()
