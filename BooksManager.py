from Tkinter import *
import tkMessageBox
import sqlite3

root = Tk()
root.title = "My Books Manager"


# ----------Methods----------
def connect():
    try:
        my_connection = sqlite3.connect("My Books Manager")
        my_cursor = my_connection.cursor()
        my_cursor.execute('''
			CREATE TABLE MYBOOKS (
			BOOK_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
			TITLE VARCHAR(100), 
			AUTHOR VARCHAR(50), 
			EDITORIAL VARCHAR(50),
			YEAR VARCHAR(4),
			COMMENTS VARCHAR(100))
			''')
        my_connection.commit()
        tkMessageBox.showinfo(message="Database successfully created", title="Info")
    except Exception:
        tkMessageBox.showerror(message="The Database already exists", title="Warning")


def close():
    answer = tkMessageBox.askquestion(message="Close the app?", title="Warning")

    if answer == "yes":
        root.destroy()


def clear_fields():
    book_id.set("")
    title.set("")
    author.set("")
    editorial.set("")
    year.set("")
    comments_field.delete(1.0, END)
    tkMessageBox.showerror(message="All fields were cleared", title="Info")


def show_about():
    tkMessageBox.showinfo(message="Version: 1.0\nAuthor: Ferran Bals", title="About")


# ----------CRUD----------

def create():
    data = [
        (title.get(), author.get(), editorial.get(), year.get(), comments_field.get(1.0, END))
    ]

    my_connection = sqlite3.connect("My Books Manager")
    my_cursor = my_connection.cursor()
    my_cursor.executemany("INSERT INTO MYBOOKS VALUES (NULL, ?, ?, ?, ?, ?)", data)
    my_connection.commit()

    tkMessageBox.showerror(message="Book added successfully", title="Info")


def read():
    data = [
        (book_id.get())
    ]

    my_connection = sqlite3.connect("My Books Manager")
    my_cursor = my_connection.cursor()
    my_cursor.execute("SELECT * FROM MYBOOKS WHERE BOOK_ID=?", data)

    library = my_cursor.fetchall()
    my_connection.commit()

    for item in library:
        title.set(item[1])
        author.set(item[2])
        editorial.set(item[3])
        year.set(item[4])
        comments_field.insert(1.0, item[5])


def update():
    data = [
        (title.get(), author.get(), editorial.get(), year.get(), comments_field.get(1.0, END), book_id.get())
    ]

    my_connection = sqlite3.connect("My Books Manager")
    my_cursor = my_connection.cursor()
    my_cursor.executemany(
        "UPDATE MYBOOKS SET TITLE=?, AUTHOR=?, EDITORIAL=?, YEAR=?, COMMENTS=? WHERE ID=?", data)
    my_connection.commit()

    tkMessageBox.showerror(message="Book updated successfully", title="Info")


def delete():
    data = [
        (book_id.get())
    ]

    my_connection = sqlite3.connect("My Books Manager")
    my_cursor = my_connection.cursor()
    my_cursor.execute("DELETE FROM MYBOOKS WHERE BOOK_ID=?", data)
    my_connection.commit()

    tkMessageBox.showerror(message="Book removed successfully", title="Info")


# ----------UpperMenu----------
barraMenu = Menu(root)
root.config(menu=barraMenu, width=300, height=300)

BBDDMenu = Menu(barraMenu, tearoff=0)
BBDDMenu.add_command(label="Connect", command=lambda: connect())
BBDDMenu.add_command(label="Close", command=lambda: close())

BorrarMenu = Menu(barraMenu, tearoff=0)
BorrarMenu.add_command(label="Clear fields", command=lambda: clear_fields())
CRUDMenu = Menu(barraMenu, tearoff=0)
CRUDMenu.add_command(label="Create", command=lambda: create())
CRUDMenu.add_command(label="Read", command=lambda: read())
CRUDMenu.add_command(label="Update", command=lambda: update())
CRUDMenu.add_command(label="Delete", command=lambda: delete())

AyudaMenu = Menu(barraMenu, tearoff=0)
AyudaMenu.add_command(label="License")
AyudaMenu.add_command(label="About...", command=lambda: show_about())

barraMenu.add_cascade(label="BBDD", menu=BBDDMenu)
barraMenu.add_cascade(label="Clear fields", menu=BorrarMenu)
barraMenu.add_cascade(label="CRUD", menu=CRUDMenu)
barraMenu.add_cascade(label="Help", menu=AyudaMenu)

# ----------Screen----------
my_frame = Frame(root, width=100, height=100)
my_frame.pack()
my_frame.config(width="650", height="650")

# ----------Fields----------
id_label = Label(my_frame, text="ID: ", fg="black")
id_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
book_id = StringVar()
id_field = Entry(my_frame, textvariable=book_id)
id_field.grid(row=0, column=1, sticky="w", padx=10, pady=10, columnspan=3)

title_label = Label(my_frame, text="Titulo: ", fg="black")
title_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)
title = StringVar()
title_field = Entry(my_frame, textvariable=title)
title_field.grid(row=1, column=1, sticky="w", padx=10, pady=10, columnspan=3)

author_label = Label(my_frame, text="Autor: ", fg="black")
author_label.grid(row=2, column=0, sticky="w", padx=10, pady=10)
author = StringVar()
author_field = Entry(my_frame, textvariable=author, fg="red", justify="right")
author_field.grid(row=2, column=1, sticky="w", padx=10, pady=10, columnspan=3)

editorial_label = Label(my_frame, text="Editorial: ", fg="black")
editorial_label.grid(row=3, column=0, sticky="w", padx=10, pady=10)
editorial = StringVar()
editorial_field = Entry(my_frame, textvariable=editorial)
editorial_field.grid(row=3, column=1, sticky="w", padx=10, pady=10, columnspan=3)

year_label = Label(my_frame, text="Anyo publicacion: ", fg="black")
year_label.grid(row=4, column=0, sticky="w", padx=10, pady=10)
year = StringVar()
year_field = Entry(my_frame, textvariable=year)
year_field.grid(row=4, column=1, sticky="w", padx=10, pady=10, columnspan=3)

comments_label = Label(my_frame, text="Comentarios: ", fg="black")
comments_label.grid(row=5, column=0, sticky="w", padx=10, pady=10)
comments_field = Text(my_frame, width=40,  height=5)
comments_field.grid(row=5, column=1, padx=10, pady=10, columnspan=3)

scrollVert = Scrollbar(my_frame, command=comments_field.yview)
scrollVert.grid(row=5, column=4, sticky="nsew")
comments_field.config(yscrollcommand=scrollVert.set)

# ----------Buttons----------
my_frame_two = Frame(root, width=100, height=100)
my_frame_two.pack()
button_create = Button(my_frame_two, text="Create", width=6, bg="black", command=lambda: create())
button_create.grid(row=0, column=0, sticky="e")
button_read = Button(my_frame_two, text="Read", width=6, command=lambda: read())
button_read.grid(row=0, column=1, sticky="e")
button_update = Button(my_frame_two, text="Update", width=6, command=lambda: update())
button_update.grid(row=0, column=2, sticky="e")
button_delete = Button(my_frame_two, text="Delete", width=6, command=lambda: delete())
button_delete.grid(row=0, column=3, sticky="e")
button_connect = Button(my_frame_two, text="Connect", width=6, command=lambda: connect())
button_connect.grid(row=1, column=0, sticky="e")

# ----------MainLoop----------
root.mainloop()
