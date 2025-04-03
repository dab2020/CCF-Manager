import customtkinter as ctk
from tkinter import *
from tkinter import ttk
from PIL import Image
from enter import importdata
from edit import editdata
from database import get_sales, get_invoice_items, get_sale_by_id, get_rooms
import os
import subprocess
import sys


# home.py
def view_old_sales():
    def edit_sale():
        selected_item = tree.selection()[0]
        sale_id = tree.item(selected_item, 'values')[0]
        sale_data = get_sale_by_id(sale_id)
        print(sale_data)
        editdata(sale_data)

    def show_invoice_items(event):
        selected_item = tree.selection()[0]
        sale_id = tree.item(selected_item, 'values')[0]
        items = get_invoice_items(sale_id)
        item_tree.delete(*item_tree.get_children())
        for item in items:
            item_tree.insert('', 'end', values=item)
        # Also update room info:
        show_room_data(sale_id)

    def show_room_data(sale_id):
        rooms = get_rooms(sale_id)
        room_tree.delete(*room_tree.get_children())
        for room in rooms:
            room_tree.insert('', 'end', values=room)

    def open_invoice_folder():
        folder_path = os.path.join(os.getcwd(), "invoice")
        if os.path.exists(folder_path):
            subprocess.Popen(f'explorer {os.path.normpath(folder_path)}')
        else:
            print(f"The folder {folder_path} does not exist.")

    def search_sales():
        search_term = search_entry.get()
        matching_sales = []
        for sale in get_sales():
            if (search_term.lower() in sale[1].lower()) or (search_term.lower() in sale[5].lower()):
                matching_sales.append(sale)
        update_sales_tree(matching_sales)

    def update_sales_tree(sales):
        tree.delete(*tree.get_children())
        for sale in sales:
            tree.insert('', 'end', values=sale)

    root = ctk.CTk()
    root.title("Old Sales")
    root.geometry("1000x600")

    # --- Main Frame (using grid for better control) ---
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=2)
    main_frame.rowconfigure(0, weight=1)

    # --- Search Bar ---
    search_frame = ctk.CTkFrame(root)
    search_frame.pack(side='top', fill='x', padx=10, pady=5)

    search_label = ctk.CTkLabel(search_frame, text="Search:")
    search_label.pack(side='left', padx=10)

    search_entry = ctk.CTkEntry(search_frame)
    search_entry.pack(side='left', fill='x', expand=True, padx=10)

    search_button = ctk.CTkButton(search_frame, text="Search", command=search_sales)
    search_button.pack(side='left', padx=10)

    # --- Sales Treeview (Left side of main_frame) ---
    sales_columns = ('id', 'name', 'phone', 'date', 'addr', 'zip')
    tree = ttk.Treeview(main_frame, columns=sales_columns, show='headings')
    for col in sales_columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=80, anchor="center")
    update_sales_tree(get_sales())
    tree.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
    tree.bind('<<TreeviewSelect>>', show_invoice_items)

    # --- Right Frame for Invoice & Room Data (placed in column 1) ---
    right_frame = ctk.CTkFrame(main_frame)
    right_frame.grid(row=0, column=1, sticky="nsew")
    right_frame.rowconfigure(0, weight=1)
    right_frame.rowconfigure(1, weight=1)
    right_frame.columnconfigure(0, weight=1)

    # Invoice Items Treeview (Top half of right_frame)
    item_frame = ctk.CTkFrame(right_frame)
    item_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    item_columns = ('type', 'desc', 'qty', 'price', 'total')
    item_tree = ttk.Treeview(item_frame, columns=item_columns, show='headings')
    for col in item_columns:
        item_tree.heading(col, text=col.capitalize())
        item_tree.column(col, width=80, anchor="center")
    item_tree.pack(fill='both', expand=True)

    # Room Data Treeview (Bottom half of right_frame)
    room_frame = ctk.CTkFrame(right_frame)
    room_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    room_columns = ('service_type', 'space_type', 'room_width', 'room_length', 'room_area')
    room_tree = ttk.Treeview(room_frame, columns=room_columns, show='headings')
    room_tree.heading('service_type', text='Service Type')
    room_tree.heading('space_type', text='Space Type')
    room_tree.heading('room_width', text='Width')
    room_tree.heading('room_length', text='Length')
    room_tree.heading('room_area', text='Area')
    for col in room_columns:
        room_tree.column(col, width=80, anchor="center")
    room_tree.pack(fill='both', expand=True)

    # --- Bottom Button Frame ---
    button_frame = ctk.CTkFrame(root)
    button_frame.pack(side='bottom', fill='x', pady=10, padx=10)

    show_invoices_button = ctk.CTkButton(button_frame, text="Show Invoices", command=open_invoice_folder)
    show_invoices_button.pack(side='left')

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
