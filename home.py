import customtkinter as ctk
from tkinter import *
from tkinter import ttk
from PIL import Image
from enter import importdata
from edit import editdata
from database import get_sales, get_invoice_items, get_sale_by_id
import os
import subprocess
import sys


# home.py
def view_old_sales():
    def edit_sale():
        selected_item = tree.selection()[0]
        sale_id = tree.item(selected_item, 'values')[0]
        sale_data = get_sale_by_id(sale_id)  # Get sale data by ID
        print(sale_data)
        editdata(sale_data)  # Open edit sale screen with data

    def show_invoice_items(event):
        selected_item = tree.selection()[0]
        sale_id = tree.item(selected_item, 'values')[0]
        items = get_invoice_items(sale_id)
        item_tree.delete(*item_tree.get_children())  # Clear existing items
        for item in items:
            item_tree.insert('', 'end', values=item[0:])

    def open_invoice_folder():
        folder_path = os.path.join(os.getcwd(), "invoice")
        if os.path.exists(folder_path):
            subprocess.Popen(f'explorer {os.path.normpath(folder_path)}')
        else:
            print(f"The folder {folder_path} does not exist.")

    def search_sales():
        search_term = search_entry.get().lower()
        matching_sales = []
        for sale in get_sales():
            if any(search_term in str(field).lower() for field in sale):
                matching_sales.append(sale)
        update_sales_tree(matching_sales)

    def update_sales_tree(sales):
        tree.delete(*tree.get_children())  # Clear existing items
        for sale in sales:
            tree.insert('', 'end', values=sale)

    root = ctk.CTk()
    root.title("Old Sales")
    root.geometry("800x600")

    frame = ctk.CTkFrame(root)
    frame.pack(expand=True, fill="both")

    search_frame = ctk.CTkFrame(root)
    search_frame.pack(side='top', fill='x')

    search_label = ctk.CTkLabel(search_frame, text="Search:")
    search_label.pack(side='left', padx=10)

    search_entry = ctk.CTkEntry(search_frame)
    search_entry.pack(side='left', fill='x', expand=True, padx=10)

    search_button = ctk.CTkButton(search_frame, text="Search", command=search_sales)
    search_button.pack(side='left', padx=10)

    columns = ('id', 'name', 'phone', 'date', 'addr', 'zip')
    tree = ttk.Treeview(frame, columns=columns, show='headings')
    tree.heading('id', text='ID')
    tree.heading('name', text='Name')
    tree.heading('phone', text='Phone')
    tree.heading('date', text='Date')
    tree.heading('addr', text='Address')
    tree.heading('zip', text='Postal Code')

    # Set column widths
    for col in columns:
        tree.column(col, width=50)

    update_sales_tree(get_sales())

    tree.pack(side='left', fill='both', expand=True)

    item_columns = ('type', 'desc', 'qty', 'price', 'total')
    item_tree = ttk.Treeview(frame, columns=item_columns, show='headings')
    item_tree.heading('type', text='Type')
    item_tree.heading('desc', text='Description')
    item_tree.heading('qty', text='Qty')
    item_tree.heading('price', text='Price')
    item_tree.heading('total', text='Total')

    # Set column widths for item tree
    for col in item_columns:
        item_tree.column(col, width=50)

    item_tree.pack(side='right', fill='both', expand=True)

    tree.bind('<<TreeviewSelect>>', show_invoice_items)

    # Add button to open invoice folder
    button_frame = ctk.CTkFrame(root)
    button_frame.pack(side='bottom', fill='x', pady=10)

    show_invoices_button = ctk.CTkButton(button_frame, text="Show Invoices", command=open_invoice_folder)
    show_invoices_button.pack(side='left')

    # Add Edit Sale button
    edit_sale_button = ctk.CTkButton(button_frame, text="Edit Sale", command=edit_sale)
    edit_sale_button.pack(side='right')
    root.mainloop()


def home():
    def gotodataentryscreen():
        importdata()

    def goto_view_sales():
        view_old_sales()

    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("green")

    root = ctk.CTk()
    root.title("CCF Manager")
    root.geometry("1000x500")
    root.iconbitmap(('cch.ico'))

    content_frame = ctk.CTkFrame(root)
    content_frame.pack(expand=True, fill="both")

    my_image = ctk.CTkImage(light_image=Image.open(('cch.png')),
                            dark_image=Image.open(('cch.png')),
                            size=(300, 174))
    my_label = ctk.CTkLabel(content_frame, text="", image=my_image)
    my_label.pack(pady=10)

    button_frame = ctk.CTkFrame(content_frame, height=100)
    button_frame.configure(fg_color="transparent")
    button_frame.pack(side="top", fill="x", pady=100)

    button_style = ctk.CTkButton(master=root)
    button_style.configure(width=200, height=40)

    add_sale_button = ctk.CTkButton(button_frame, text="Add a new sale", font=("Arial", 18), width=200, height=40,
                                    border_width=0, command=gotodataentryscreen)
    add_sale_button.pack(side="left", padx=100)

    view_sale_button = ctk.CTkButton(button_frame, text="View old sale", font=("Arial", 18), width=200, height=40,
                                     border_width=0, command=goto_view_sales)
    view_sale_button.pack(side="right", padx=100)

    root.mainloop()
