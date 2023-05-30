import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox

db_host = 'localhost'
db_user = 'JohnDoe'
db_password = '1234'

database = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password
)

db_cursor = database.cursor()

db_cursor.execute("CREATE DATABASE IF NOT EXISTS lab9_db")
db_cursor.close()

# Establishing connection to the database
connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database='lab9_db'
)

table_cursor = connection.cursor()

# Creating the table if it doesn't exist
table_cursor.execute('''CREATE TABLE IF NOT EXISTS MarvelInfo(
                            ID int(3) NOT NULL,
                            Movie varchar(80) NOT NULL,
                            DateInfo varchar(50) NOT NULL,
                            Mcu_Phase varchar(50)
                        )''')

id_list = []
data_holder = {}

# Reading data from file and inserting into the database
with open("Marvel.txt", 'r') as file:
    for line in file:
        line = line.strip()
        if line:
            movie_info = line.split()
            movie_id = int(movie_info[0])
            movie_name = movie_info[1]
            date_info = movie_info[2]
            mcu_phase = movie_info[3]
            id_list.append(movie_id)
            data_holder[movie_id] = movie_name
            sql_insert = """INSERT INTO MarvelInfo (ID,Movie,DateInfo,Mcu_Phase)
                                                      VALUES (%s,%s,%s,%s)"""
            values = (movie_id, movie_name, date_info, mcu_phase)
            table_cursor.execute(sql_insert, values)

connection.commit()

def update_text_box(*args):
    selected_item = dropdown_var.get()
    for key in data_holder.keys():
        if selected_item == 'ID':
            text_box.delete(0, tk.END)
            break
        if int(key) == int(selected_item):
            text_box.delete(0, tk.END)
            text_box.insert(tk.END, data_holder[key])
            break

def add_to_database(id_entry, movie_entry, date_entry, phase_entry):
    id_value = id_entry.get()
    movie_value = movie_entry.get()
    date_value = date_entry.get()
    phase_value = phase_entry.get()
    with open("Marvel.txt", 'a') as file:
        file.write("\n" + id_value + " " + movie_value + " " + date_value + " " + phase_value)
    sql_insert = """INSERT INTO MarvelInfo (ID,Movie,DateInfo,Mcu_Phase)
                                                          VALUES (%s,%s,%s,%s)"""
    values = (id_value, movie_value, date_value, phase_value)
    table_cursor.execute(sql_insert, values)
    connection.commit()
    if id_value and movie_value and date_value and phase_value:
        messagebox.showinfo("Success", "Data added to the database!")
    else:
        messagebox.showwarning("Error", "Please fill in all fields!")

def open_popup_box():
    popup_box = tk.Toplevel(window)
    popup_box.title("Add Data")
    popup_box.geometry("500x300")

    id_label = tk.Label(popup_box, text="ID=")
    id_label.pack()

    id_entry = tk.Entry(popup_box)
    id_entry.pack()

    movie_label = tk.Label(popup_box, text="Movie:")
    movie_label.pack()

    movie_entry = tk.Entry(popup_box)
    movie_entry.pack()

    date_label = tk.Label(popup_box, text="Date:")
    date_label.pack()

    date_entry = tk.Entry(popup_box)
    date_entry.pack()

    phase_label = tk.Label(popup_box, text="MCU Phase:")
    phase_label.pack()

    phase_entry = tk.Entry(popup_box)
    phase_entry.pack()

    ok_button = tk.Button(popup_box, text="Ok",
                          command=lambda: add_to_database(id_entry, movie_entry, date_entry, phase_entry))
    ok_button.pack(side=tk.LEFT, padx=10)

    cancel_button = tk.Button(popup_box, text="Cancel", command=popup_box.destroy)
    cancel_button.pack(side=tk.RIGHT, padx=10)

def list_all_data():
    table_cursor.execute("SELECT * FROM MarvelInfo")
    result = table_cursor.fetchall()
    list_window = tk.Toplevel()
    list_window.title("All Data")
    text_box = tk.Text(list_window, width=30, height=30)
    text_box.pack()
    for row in result:
        text_box.insert(tk.END, f"ID: {row[0]}\n")
        text_box.insert(tk.END, f"Movie: {row[1]}\n")
        text_box.insert(tk.END, f"Date: {row[2]}\n")
        text_box.insert(tk.END, f"MCU Phase: {row[3]}\n")
        text_box.insert(tk.END, "\n")

window = tk.Tk()
window.title('Marvel')

box_frame = ttk.Frame(window, padding="20")
box_frame.grid(row=0, column=0)

button1 = ttk.Button(box_frame, text="Add Data", command=open_popup_box)
button1.grid(row=0, column=0, padx=5, pady=5)

button2 = ttk.Button(box_frame, text="List All Data", command=list_all_data)
button2.grid(row=0, column=1, padx=5, pady=5)

text_box = ttk.Entry(box_frame, width=30)
text_box.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

dropdown_var = tk.StringVar()
dropdown_var.trace('w', update_text_box)
dropdown = ttk.Combobox(box_frame, textvariable=dropdown_var)
dropdown['values'] = ["ID"] + [i for i in range(1, id_list[-1] + 1)]
dropdown.current(0)
dropdown.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

window.mainloop()
connection.close()
table_cursor.close()
