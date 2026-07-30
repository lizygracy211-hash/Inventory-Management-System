from tkinter import *
from tkinter import ttk, messagebox
import database

# Create database
database.connect()

root = Tk()
root.title("Inventory Management System")
root.geometry("850x500")
root.resizable(False, False)

selected_id = None

title = Label(
    root,
    text="Inventory Management System",
    font=("Arial", 20, "bold"),
    bg="#2E86C1",
    fg="white",
    pady=10
)
title.pack(fill=X)

frame = Frame(root)
frame.pack(pady=20)
search_var = StringVar()

Label(root, text="Search").pack()

Entry(root, textvariable=search_var, width=30).pack()

Label(frame, text="Product Name").grid(row=0, column=0, padx=10, pady=10)
product_name = Entry(frame, width=25)
product_name.grid(row=0, column=1)

Label(frame, text="Category").grid(row=1, column=0, padx=10, pady=10)
category = Entry(frame, width=25)
category.grid(row=1, column=1)

Label(frame, text="Quantity").grid(row=2, column=0, padx=10, pady=10)
quantity = Entry(frame, width=25)
quantity.grid(row=2, column=1)

Label(frame, text="Price").grid(row=3, column=0, padx=10, pady=10)
price = Entry(frame, width=25)
price.grid(row=3, column=1)

def load_data():
    table.delete(*table.get_children())
    for row in database.get_products():
        table.insert("", END, values=row)


def add_product():
    if product_name.get() == "" or category.get() == "" or quantity.get() == "" or price.get() == "":
        messagebox.showerror("Error", "Please fill all fields")
        return

    database.add_product(
        product_name.get(),
        category.get(),
        quantity.get(),
        price.get()
    )

    messagebox.showinfo("Success", "Product Added Successfully")

    product_name.delete(0, END)
    category.delete(0, END)
    quantity.delete(0, END)
    price.delete(0, END)

    load_data()

def select_product(event):
    global selected_id

    selected = table.focus()

    if selected == "":
        return

    values = table.item(selected, "values")

    selected_id = values[0]

    product_name.delete(0, END)
    category.delete(0, END)
    quantity.delete(0, END)
    price.delete(0, END)

    product_name.insert(0, values[1])
    category.insert(0, values[2])
    quantity.insert(0, values[3])
    price.insert(0, values[4])


def update_product():
    global selected_id

    if selected_id is None:
        messagebox.showerror("Error", "Select a product first")
        return

    database.update_product(
        selected_id,
        product_name.get(),
        category.get(),
        quantity.get(),
        price.get()
    )

    load_data()

    messagebox.showinfo("Success", "Product Updated Successfully")

def delete_product():
    selected = table.focus()

    if selected == "":
        messagebox.showerror("Error", "Select a product")
        return

    values = table.item(selected, "values")

    database.delete_product(values[0])

    load_data()

    messagebox.showinfo("Success", "Product Deleted Successfully")

def search_product():
    table.delete(*table.get_children())

    rows = database.search_product(search_var.get())

    for row in rows:
        table.insert("", END, values=row)

Button(
    frame,
    text="Add Product",
    width=20,
    bg="green",
    fg="white",
    command=add_product
).grid(row=4, column=0, columnspan=2, pady=15)

Button(
    frame,
    text="Delete Product",
    width=20,
    bg="red",
    fg="white",
    command=delete_product
).grid(row=4, column=2, padx=10)

Button(
    frame,
    text="Update Product",
    width=20,
    bg="blue",
    fg="white",
    command=update_product
).grid(row=4, column=3, padx=10)

Button(
    root,
    text="Search",
    bg="orange",
    fg="white",
    command=search_product
).pack(pady=5)

table = ttk.Treeview(
    root,
    columns=("ID", "Product", "Category", "Quantity", "Price"),
    show="headings",
    height=10
)

table.heading("ID", text="ID")
table.heading("Product", text="Product")
table.heading("Category", text="Category")
table.heading("Quantity", text="Quantity")
table.heading("Price", text="Price")

table.column("ID", width=50)
table.column("Product", width=180)
table.column("Category", width=150)
table.column("Quantity", width=120)
table.column("Price", width=120)

table.pack(pady=20)
table.bind("<<TreeviewSelect>>", select_product)

load_data()



root.mainloop()