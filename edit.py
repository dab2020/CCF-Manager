import customtkinter as ctk
from tkinter import ttk
from customerdocgen import generatecustomerinvoice, generateinstall
from database import save_sale, get_invoice_items, update_sale
from datetime import date
from housekeeping import incvalue
import sys
import os
from tkcalendar import DateEntry


def editdata(sale_data):

    def makepdfcustomerinvoice():
        name = first_name_entry.get() + " " + last_name_entry.get()
        phone = phone_entry.get()
        address = address_entry.get()
        parking = parking_combobox.get()
        zipcode = zip_entry.get()
        otherinfo = other_info_textbox.get("1.0", "end-1c")
        rminfos = roominfo
        current_items = []
        for item in tree.get_children():
            values = tree.item(item)['values']
            current_items.append(values)

        invoice_list = current_items
        installernm = inst_entry.get()
        deldate1 = deldate_entry.get()
        fitdate1 = fitdate_entry.get()
        paymeth = meth_type_combobox.get()
        vetflag = vetcheckbutton.get()
        depflag = depcheckbutton.get()
        uniqueid = sale_data[0]
        total = 0.0
        for row in invoice_list:
            total += float(row[4])

        today = date.today().strftime('%B %d, %Y')
        update_sale(uniqueid, name, phone, today, address, parking, total, invoice_list, zipcode)
        print("Bout to print")
        generatecustomerinvoice(name, phone, invoice_list, total, paymeth, vetflag, depflag, uniqueid, zipcode, address)

    def makepdfinstaller():
        name = first_name_entry.get() + " " + last_name_entry.get()
        phone = phone_entry.get()
        address = address_entry.get()
        parking = parking_combobox.get()
        zipcode = zip_entry.get()
        otherinfo = other_info_textbox.get("1.0", "end-1c")
        rminfos = roominfo
        product = invoice_list
        installernm = inst_entry.get()
        deldate1 = deldate_entry.get()
        fitdate1 = fitdate_entry.get()
        total = 0
        for row in product:
            total += row[4]

        today = date.today().strftime('%B %d, %Y')
        generateinstall(name, phone, product, parking, zipcode, rminfos, installernm, address, deldate1, fitdate1,
                        otherinfo)

    def validate_integer(P):
        if P.isdigit() or P == "":
            return True
        return False

    def validate_float(P):
        try:
            if P == "" or float(P):
                return True
        except ValueError:
            return False
        return False

    def validate_unit(P):
        try:
            if P == "" or float(P) >= 0:
                return True
        except ValueError:
            return False
        return False

    def buttonclick():
        print(invoice_list)

    # Create main window and set it to open full screen
    window = ctk.CTk()
    window.title("Data Entry Form")
    window.state("zoomed")  # Opens the window maximized/full screen

    # Configure grid for the main window so that frames expand nicely
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_rowconfigure(0, weight=1)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="#2e2e2e",
                    foreground="#2b2b2b",
                    fieldbackground="#2e2e2e",
                    bordercolor="green",
                    borderwidth=1)
    style.map("Treeview",
              background=[('selected', '#2b2b2b')])

    # Left and right main frames
    frame_left = ctk.CTkFrame(window)
    frame_left.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
    frame_right = ctk.CTkFrame(window)
    frame_right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    # Make sure the frames expand with the window
    frame_left.grid_rowconfigure(3, weight=1)
    frame_right.grid_rowconfigure(2, weight=1)
    frame_right.grid_columnconfigure(0, weight=1)

    # --- LEFT SIDE: User Info, Room Info and Other Info ---
    user_info_frame = ctk.CTkFrame(frame_left)
    user_info_frame.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="ew")
    user_info_frame.grid_columnconfigure((0, 1, 2), weight=1)

    first_name_label = ctk.CTkLabel(user_info_frame, text="First Name")
    first_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    last_name_label = ctk.CTkLabel(user_info_frame, text="Last Name")
    last_name_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    phone_label = ctk.CTkLabel(user_info_frame, text="Phone Number")
    phone_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")

    first_name_entry = ctk.CTkEntry(user_info_frame)
    last_name_entry = ctk.CTkEntry(user_info_frame)
    first_name_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
    last_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    phone_entry = ctk.CTkEntry(user_info_frame)
    phone_entry.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

    address_label = ctk.CTkLabel(user_info_frame, text="Address")
    address_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    address_entry = ctk.CTkEntry(user_info_frame)
    address_entry.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

    zip_label = ctk.CTkLabel(user_info_frame, text="Post Code")
    zip_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    zip_entry = ctk.CTkEntry(user_info_frame)
    zip_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    parking_label = ctk.CTkLabel(user_info_frame, text="Parking")
    parking_combobox = ctk.CTkComboBox(user_info_frame, values=["Driveway", "Onstreet", "Paid", "No Parking"])
    parking_label.grid(row=2, column=2, padx=10, pady=5, sticky="w")
    parking_combobox.grid(row=3, column=2, padx=10, pady=5, sticky="ew")

    room_info_frame = ctk.CTkFrame(frame_left)
    room_info_frame.grid(row=2, column=0, padx=20, pady=(10, 5), sticky="ew")
    room_info_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

    service_type_label = ctk.CTkLabel(room_info_frame, text="Type of Service")
    service_type_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    service_type_combobox = ctk.CTkComboBox(room_info_frame,
                                            values=["Carpet", "Laminate", "Wood", "Vinyl tile", "Other"])
    service_type_combobox.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    space_type_label = ctk.CTkLabel(room_info_frame, text="Type of Space")
    space_type_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    space_type_combobox = ctk.CTkComboBox(room_info_frame, values=["Room", "Living Room", "Hallway", "Stairs", "Commercial Flooring"])
    space_type_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    room_width_label = ctk.CTkLabel(room_info_frame, text="Width (ft)")
    room_width_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")
    room_width_entry = ctk.CTkEntry(room_info_frame, validate="key",
                                    validatecommand=(window.register(validate_unit), '%P'))
    room_width_entry.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

    room_length_label = ctk.CTkLabel(room_info_frame, text="Length (ft)")
    room_length_label.grid(row=0, column=3, padx=10, pady=5, sticky="w")
    room_length_entry = ctk.CTkEntry(room_info_frame, validate="key",
                                     validatecommand=(window.register(validate_unit), '%P'))
    room_length_entry.grid(row=1, column=3, padx=10, pady=5, sticky="ew")

    add_room_button = ctk.CTkButton(room_info_frame, text="Add Room",
                                    command=lambda: add_room(tree_rooms, service_type_combobox, space_type_combobox,
                                                             room_width_entry, room_length_entry))
    add_room_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    delete_room_button = ctk.CTkButton(room_info_frame, text="Delete Entry", command=lambda: delete_latest_room_entry())
    delete_room_button.grid(row=2, column=2, columnspan=2, padx=10, pady=5, sticky="ew")

    columns_rooms = ['service_type', 'space_type', 'room_width', 'room_length', 'area']
    tree_rooms = ttk.Treeview(frame_left, columns=columns_rooms, show="headings", style="Treeview")
    tree_rooms.heading('service_type', text='Type of Service')
    tree_rooms.heading('space_type', text='Type of Space')
    tree_rooms.heading('room_width', text='Width (ft)')
    tree_rooms.heading('room_length', text='Length (ft)')
    tree_rooms.heading('area', text='Area (sqft)')

    tree_rooms.column('service_type', width=100)
    tree_rooms.column('space_type', width=100)
    tree_rooms.column('room_width', width=50)
    tree_rooms.column('room_length', width=50)
    tree_rooms.column('area', width=50)

    tree_rooms.grid(row=3, column=0, padx=20, pady=(10, 10), sticky="nsew")

    roominfo = []

    other_info_label = ctk.CTkLabel(frame_left, text="Other Information")
    other_info_label.grid(row=4, column=0, padx=10, pady=(10, 5), sticky="w")
    other_info_textbox = ctk.CTkTextbox(frame_left, width=200, height=100)
    other_info_textbox.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

    # --- RIGHT SIDE: Item Info and Additional Details ---
    carpet_info_frame = ctk.CTkFrame(frame_right)
    carpet_info_frame.grid(row=3, column=0, padx=20, pady=(10, 5), sticky="ew")
    carpet_info_frame.grid_columnconfigure((0, 6), weight=1)

    new_button2 = ctk.CTkButton(carpet_info_frame, text="Generate Customer Invoice", command=makepdfcustomerinvoice)
    new_button2.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

    new_button = ctk.CTkButton(carpet_info_frame, text="Generate Installer Copy", command=makepdfinstaller)
    new_button.grid(row=4, column=6, padx=10, pady=5, sticky="ew")

    item2_info_frame = ctk.CTkFrame(frame_right)
    item2_info_frame.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="ew")
    item2_info_frame.grid_columnconfigure((0, 1, 2), weight=1)

    deldate_label = ctk.CTkLabel(item2_info_frame, text="Delivery Date")
    deldate_entry = DateEntry(item2_info_frame, date_pattern="dd-mm-yyyy")
    deldate_label.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    deldate_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    fitdate_label = ctk.CTkLabel(item2_info_frame, text="Fitting Date")
    fitdate_entry = DateEntry(item2_info_frame, date_pattern="dd-mm-yyyy")
    fitdate_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")
    fitdate_entry.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

    inst_label = ctk.CTkLabel(item2_info_frame, text="Installer:")
    inst_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    inst_entry = ctk.CTkEntry(item2_info_frame)
    inst_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    meth_type_label = ctk.CTkLabel(item2_info_frame, text="Method of Payment")
    meth_type_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    meth_type_combobox = ctk.CTkComboBox(item2_info_frame, values=["Cash", "Card", "Bank Transfer"])
    meth_type_combobox.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

    vetcheckbutton = ctk.CTkCheckBox(item2_info_frame, text="VET (20%)",
                                     onvalue=True, offvalue=False)
    vetcheckbutton.grid(row=3, column=1, padx=10, pady=5)

    depcheckbutton = ctk.CTkCheckBox(item2_info_frame, text="Deposit (50%)",
                                     onvalue=True, offvalue=False)
    depcheckbutton.grid(row=3, column=2, padx=10, pady=5)

    item_info_frame = ctk.CTkFrame(frame_right)
    item_info_frame.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="ew")
    item_info_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

    serv_type_label = ctk.CTkLabel(item_info_frame, text="Type of Service")
    serv_type_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    serv_type_combobox = ctk.CTkComboBox(item_info_frame, values=["Carpet", "Vinyl", "Laminate", "Wood Flooring",
                                                                  "Commercial Flooring", "Underlay", "Grippers",
                                                                  "Door Bars", "Carpet Removal", "Furniture Moving",
                                                                  "Other"])
    serv_type_combobox.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    qty_label = ctk.CTkLabel(item_info_frame, text="Qty")
    qty_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")
    qty_spinbox = ctk.CTkEntry(item_info_frame, validate="key",
                               validatecommand=(window.register(validate_integer), '%P'))
    qty_spinbox.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

    desc_label = ctk.CTkLabel(item_info_frame, text="Name of Product")
    desc_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    desc_entry = ctk.CTkEntry(item_info_frame)
    desc_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    price_label = ctk.CTkLabel(item_info_frame, text="Unit Price")
    price_label.grid(row=0, column=3, padx=10, pady=5, sticky="w")
    price_spinbox = ctk.CTkEntry(item_info_frame, validate="key",
                                 validatecommand=(window.register(validate_unit), '%P'))
    price_spinbox.grid(row=1, column=3, padx=10, pady=5, sticky="ew")

    add_item_button = ctk.CTkButton(item_info_frame, text="Add item",
                                    command=lambda: add_item(tree, serv_type_combobox, qty_spinbox, desc_entry,
                                                             price_spinbox))
    add_item_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
    delete_item_button = ctk.CTkButton(item_info_frame, text="Delete Entry", command=lambda: delete_latest_item_entry())
    delete_item_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    columns = ('service', 'desc', 'qty', 'price', 'total')
    tree = ttk.Treeview(frame_right, columns=columns, show="headings", style="Treeview")
    tree.heading('service', text='Type of Service')
    tree.heading('desc', text='Name of Product')
    tree.heading('qty', text='Qty')
    tree.heading('price', text='Unit Price')
    tree.heading('total', text='Total')

    tree.column('qty', width=100, anchor='center')
    tree.column('desc', width=200, anchor='center')
    tree.column('price', width=100, anchor='center')
    tree.column('total', width=100, anchor='center')
    tree.column('service', width=100, anchor='center')
    invoice_list = get_invoice_items(sale_data[0])
    # for item in invoice_list:
    #     tree.insert('', 'end', values=item[2:])

    tree.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

    # Pre-populate entries with sale_data
    first_name_entry.insert(0, sale_data[1].split()[0])
    last_name_entry.insert(0, sale_data[1].split()[1])
    phone_entry.insert(0, sale_data[2])
    address_entry.insert(0, sale_data[4])
    zip_entry.insert(0, sale_data[5])
    parking_combobox.set(sale_data[6])

    # --- Utility functions ---
    def clear_item():
        qty_spinbox.delete(0, ctk.END)
        qty_spinbox.insert(0, "1")
        desc_entry.delete(0, ctk.END)
        price_spinbox.delete(0, ctk.END)
        price_spinbox.insert(0, "0.0")

    def clear_room_entries():
        service_type_combobox.set("")
        space_type_combobox.set("")
        room_width_entry.delete(0, ctk.END)
        room_length_entry.delete(0, ctk.END)

    def add_item(tree, serv_type_combobox, qty_spinbox, desc_entry, price_spinbox):
        ser = serv_type_combobox.get()
        desc = desc_entry.get()
        qty = int(qty_spinbox.get())
        price = float(price_spinbox.get())
        line_total = qty * price
        invoice_item = [ser, desc, qty, price, line_total]
        tree.insert('', 'end', values=invoice_item)
        clear_item()

    def add_room(tree_rooms, service_type_combobox, space_type_combobox, room_width_entry, room_length_entry):
        service_type = service_type_combobox.get()
        space_type = space_type_combobox.get()
        room_width = float(room_width_entry.get())
        room_length = float(room_length_entry.get())
        rmarea = room_width * room_length
        room_info_item = [service_type, space_type, room_width, room_length, rmarea]
        tree_rooms.insert('', 0, values=room_info_item)
        clear_room_entries()
        roominfo.append(room_info_item)

    def delete_latest_room_entry():
        if tree_rooms.get_children():
            latest_entry = tree_rooms.get_children()[0]
            tree_rooms.delete(latest_entry)
            roominfo.pop(0)

    def delete_latest_item_entry():
        if tree.get_children():
            latest_entry = tree.get_children()[0]
            tree.delete(latest_entry)
            # If you maintain a separate invoice_list, update it as well:
            if invoice_list:
                invoice_list.pop(0)

    window.mainloop()


# To call the form for editing, pass the appropriate sale_data object/list.
# For example:
# sale_data = [123, "John Doe", "555-1234", ...]  # Populate with actual data from your database
# editdata(sale_data)
