import customtkinter as ctk
from tkinter import ttk
from customerdocgen import generatecustomerinvoice, generateinstall
from database import save_sale
from datetime import date
from housekeeping import incvalue
from tkcalendar import DateEntry

# Initialize the global discount variable
discount_amount = 0.0

def importdata():
    global discount_amount  # Ensure we refer to the global variable in this scope

    # --------------------- Callback Functions ---------------------
    def makepdfcustomerinvoice():
        global discount_amount  # Use the updated global discount value

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
        paymeth = meth_type_combobox.get()
        uniqueid = incvalue()
        vetflag = vetcheckbutton.get()
        depflag = depcheckbutton.get()
        total = sum(row[4] for row in invoice_list)
        dayyan = discount_amount  # Assign the current discount amount
        print("Dayyan is " + str(dayyan))

        today = date.today().strftime('%B %d, %Y')
        save_sale(uniqueid, name, phone, today, address, parking, total, invoice_list, zipcode, roominfo)
        print("Bout to print customer invoice...")
        generatecustomerinvoice(name, phone, invoice_list, total, paymeth, vetflag, depflag, uniqueid, zipcode, address, dayyan)

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
        total = sum(row[4] for row in invoice_list)

        today = date.today().strftime('%B %d, %Y')
        print("Bout to print installer copy...")
        generateinstall(name, phone, product, parking, zipcode, rminfos, installernm, address, deldate1, fitdate1, otherinfo)

    def validate_integer(P):
        return P.isdigit() or P == ""

    def validate_unit(P):
        try:
            if P == "" or float(P) >= 0:
                return True
        except ValueError:
            return False
        return False

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

    # Recalculate total directly from the tree's items.
    def update_total():
        total_value = 0.0
        for child in tree.get_children():
            values = tree.item(child, 'values')
            try:
                total_value += float(values[4])
            except (IndexError, ValueError):
                continue
        total_label.configure(text=f"Total: £{total_value:.2f}")
        return total_value  # Return original total for discount calculations

    def add_item():
        try:
            qty = int(qty_spinbox.get())
            desc = desc_entry.get()
            price = float(price_spinbox.get())
        except ValueError:
            print("Invalid item entry!")
            return
        line_total = qty * price
        ser = serv_type_combobox.get()
        invoice_item = [ser, desc, qty, price, line_total]
        tree.insert('', 0, values=invoice_item)
        clear_item()
        invoice_list.append(invoice_item)
        print("Added item:", invoice_item)
        update_total()

    def add_room():
        try:
            service_type = service_type_combobox.get()
            space_type = space_type_combobox.get()
            room_width = float(room_width_entry.get())
            room_length = float(room_length_entry.get())
        except ValueError:
            print("Invalid room dimensions!")
            return
        rmarea = room_width * room_length
        room_info_item = [service_type, space_type, room_width, room_length, rmarea]
        tree_rooms.insert('', 0, values=room_info_item)
        clear_room_entries()
        roominfo.append(room_info_item)
        print("Added room:", room_info_item)

    def delete_latest_room_entry():
        if tree_rooms.get_children():
            latest_entry = tree_rooms.get_children()[0]
            tree_rooms.delete(latest_entry)
            if roominfo:
                roominfo.pop(0)

    def delete_latest_item_entry():
        if tree.get_children():
            latest_entry = tree.get_children()[0]
            tree.delete(latest_entry)
            if invoice_list:
                invoice_list.pop(0)
            update_total()

    # New function: Apply discounts and update the discounted total.
    def apply_discount():
        global discount_amount  # Ensure we're modifying the global variable

        original_total = update_total()  # Get current total from tree
        try:
            lumpsum = float(discount_lumpsum_entry.get()) if discount_lumpsum_entry.get() else 0.0
        except ValueError:
            lumpsum = 0.0
        try:
            percent = float(discount_percentage_entry.get()) if discount_percentage_entry.get() else 0.0
        except ValueError:
            percent = 0.0

        discount_amount = lumpsum + (original_total * (percent / 100))
        new_total = original_total - discount_amount
        if new_total < 0:
            new_total = 0.0
        discounted_total_label.configure(text=f"Discounted Total: £{new_total:.2f}")

    # --------------------- Main Window ---------------------
    window = ctk.CTk()
    window.title("Data Entry Form")
    window.minsize(1200, 700)

    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

    # --------------------- LEFT SECTION ---------------------
    frame_left = ctk.CTkFrame(window)
    frame_left.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    frame_left.grid_rowconfigure(2, weight=0)

    # User Info Frame with consistent alignment for labels and entry fields
    user_info_frame = ctk.CTkFrame(frame_left)
    user_info_frame.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="ew")
    for i in range(3):
        user_info_frame.grid_columnconfigure(i, weight=1)

    # Row 0: Labels for First Name, Last Name, Phone Number
    first_name_label = ctk.CTkLabel(user_info_frame, text="First Name")
    first_name_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
    last_name_label = ctk.CTkLabel(user_info_frame, text="Last Name")
    last_name_label.grid(row=0, column=1, sticky="w", padx=5, pady=5)
    phone_label = ctk.CTkLabel(user_info_frame, text="Phone Number")
    phone_label.grid(row=0, column=2, sticky="w", padx=5, pady=5)

    # Row 1: Entry fields for First Name, Last Name, Phone Number
    first_name_entry = ctk.CTkEntry(user_info_frame)
    first_name_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
    last_name_entry = ctk.CTkEntry(user_info_frame)
    last_name_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
    phone_entry = ctk.CTkEntry(user_info_frame)
    phone_entry.grid(row=1, column=2, sticky="ew", padx=5, pady=5)

    # Row 2: Labels for Address, Post Code, Parking
    address_label = ctk.CTkLabel(user_info_frame, text="Address")
    address_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
    zip_label = ctk.CTkLabel(user_info_frame, text="Post Code")
    zip_label.grid(row=2, column=1, sticky="w", padx=5, pady=5)
    parking_label = ctk.CTkLabel(user_info_frame, text="Parking")
    parking_label.grid(row=2, column=2, sticky="w", padx=5, pady=5)

    # Row 3: Entry fields for Address, Post Code, and ComboBox for Parking
    address_entry = ctk.CTkEntry(user_info_frame)
    address_entry.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
    zip_entry = ctk.CTkEntry(user_info_frame)
    zip_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
    parking_combobox = ctk.CTkComboBox(user_info_frame, values=["Driveway", "Onstreet", "Paid", "No Parking"])
    parking_combobox.grid(row=3, column=2, sticky="ew", padx=5, pady=5)

    # Room Info Frame
    room_info_frame = ctk.CTkFrame(frame_left)
    room_info_frame.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="ew")
    room_info_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

    service_type_label = ctk.CTkLabel(room_info_frame, text="Type of Service")
    service_type_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    service_type_combobox = ctk.CTkComboBox(room_info_frame,
                                            values=["Carpet", "Laminate", "Wood", "Vinyl tile", "Other"])
    service_type_combobox.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    space_type_label = ctk.CTkLabel(room_info_frame, text="Type of Space")
    space_type_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    space_type_combobox = ctk.CTkComboBox(room_info_frame,
                                          values=["Room", "Living Room", "Hallway", "Stairs", "Commercial Flooring"])
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

    add_room_button = ctk.CTkButton(room_info_frame, text="Add Room", command=add_room)
    add_room_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    delete_room_button = ctk.CTkButton(room_info_frame, text="Delete Room", command=delete_latest_room_entry)
    delete_room_button.grid(row=2, column=2, columnspan=2, padx=10, pady=5, sticky="ew")

    # Treeview for Rooms
    columns_rooms = ['service_type', 'space_type', 'room_width', 'room_length', 'area']
    tree_rooms = ttk.Treeview(frame_left, columns=columns_rooms, show="headings")
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

    tree_rooms.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="nsew")

    # Other Information
    other_info_label = ctk.CTkLabel(frame_left, text="Other Information")
    other_info_label.grid(row=3, column=0, padx=10, pady=(10, 5), sticky="w")
    other_info_textbox = ctk.CTkTextbox(frame_left, width=200, height=100)
    other_info_textbox.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

    roominfo = []  # List to store room info entries

    # --------------------- RIGHT SECTION ---------------------
    frame_right = ctk.CTkFrame(window)
    frame_right.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
    frame_right.grid_rowconfigure(3, weight=0)

    # Installer and Payment Info (Item2 Info Frame)
    item2_info_frame = ctk.CTkFrame(frame_right)
    item2_info_frame.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="ew")
    item2_info_frame.grid_columnconfigure((0, 1, 2), weight=1)

    inst_label = ctk.CTkLabel(item2_info_frame, text="Installer:")
    inst_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    inst_entry = ctk.CTkEntry(item2_info_frame)
    inst_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    # Delivery Date
    deldate_label = ctk.CTkLabel(item2_info_frame, text="Delivery Date")
    deldate_label.grid(row=0, column=1, padx=(0,10), pady=5, sticky="ew")
    deldate_entry = DateEntry(item2_info_frame, date_pattern="dd-mm-yyyy")
    deldate_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    # Fitting Date
    fitdate_label = ctk.CTkLabel(item2_info_frame, text="Fitting Date")
    fitdate_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")
    fitdate_entry = DateEntry(item2_info_frame, date_pattern="dd-mm-yyyy")
    fitdate_entry.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

    meth_type_label = ctk.CTkLabel(item2_info_frame, text="Method of Payment")
    meth_type_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    meth_type_combobox = ctk.CTkComboBox(item2_info_frame, values=["Cash", "Card", "Bank Transfer"])
    meth_type_combobox.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

    vetcheckbutton = ctk.CTkCheckBox(item2_info_frame, text="VET (20%)", onvalue=True, offvalue=False)
    vetcheckbutton.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    depcheckbutton = ctk.CTkCheckBox(item2_info_frame, text="Deposit (50%)", onvalue=True, offvalue=False)
    depcheckbutton.grid(row=3, column=2, padx=10, pady=5, sticky="w")

    # Invoice Generation Buttons (Carpet Info Frame)
    carpet_info_frame = ctk.CTkFrame(frame_right)
    carpet_info_frame.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="ew")
    carpet_info_frame.grid_columnconfigure((0, 1), weight=1)

    new_button2 = ctk.CTkButton(carpet_info_frame, text="Generate Customer Invoice", command=makepdfcustomerinvoice)
    new_button2.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    new_button = ctk.CTkButton(carpet_info_frame, text="Generate Installer Copy", command=makepdfinstaller)
    new_button.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    # Item (Product) Info Frame
    item_info_frame = ctk.CTkFrame(frame_right)
    item_info_frame.grid(row=2, column=0, padx=20, pady=(10, 5), sticky="ew")
    item_info_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

    serv_type_label = ctk.CTkLabel(item_info_frame, text="Type of Service")
    serv_type_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    serv_type_combobox = ctk.CTkComboBox(item_info_frame, values=["Carpet", "Vinyl", "Laminate", "Wood Flooring",
                                                                  "Commercial Flooring", "Underlay", "Grippers",
                                                                  "Door Bars", "Carpet Removal", "Furniture Moving",
                                                                  "Other"])
    serv_type_combobox.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    desc_label = ctk.CTkLabel(item_info_frame, text="Name of Product")
    desc_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    desc_entry = ctk.CTkEntry(item_info_frame)
    desc_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    qty_label = ctk.CTkLabel(item_info_frame, text="Qty")
    qty_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")
    qty_spinbox = ctk.CTkEntry(item_info_frame, validate="key",
                               validatecommand=(window.register(validate_integer), '%P'))
    qty_spinbox.grid(row=1, column=2, padx=10, pady=5, sticky="ew")
    qty_spinbox.insert(0, "1")

    price_label = ctk.CTkLabel(item_info_frame, text="Unit Price")
    price_label.grid(row=0, column=3, padx=10, pady=5, sticky="w")
    price_spinbox = ctk.CTkEntry(item_info_frame, validate="key",
                                 validatecommand=(window.register(validate_unit), '%P'))
    price_spinbox.grid(row=1, column=3, padx=10, pady=5, sticky="ew")
    price_spinbox.insert(0, "0.0")

    add_item_button = ctk.CTkButton(item_info_frame, text="Add item", command=add_item)
    add_item_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
    delete_item_button = ctk.CTkButton(item_info_frame, text="Delete Item", command=delete_latest_item_entry)
    delete_item_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    # Treeview for Invoice Items (services table)
    columns = ('service', 'desc', 'qty', 'price', 'total')
    tree = ttk.Treeview(frame_right, columns=columns, show="headings", height=8)
    tree.heading('service', text='Type of Service')
    tree.heading('desc', text='Name of Product')
    tree.heading('qty', text='Qty')
    tree.heading('price', text='Unit Price')
    tree.heading('total', text='Total')

    tree.column('service', width=100, anchor='center')
    tree.column('desc', width=200, anchor='center')
    tree.column('qty', width=100, anchor='center')
    tree.column('price', width=100, anchor='center')
    tree.column('total', width=100, anchor='center')

    tree.grid(row=3, column=0, padx=20, pady=(10, 5), sticky="ew")

    total_label = ctk.CTkLabel(frame_right, text="Total: £0.00", font=("Arial", 16))
    total_label.grid(row=4, column=0, padx=20, pady=(5, 10), sticky="e")

    # --- Discount Section ---
    discount_frame = ctk.CTkFrame(frame_right)
    discount_frame.grid(row=5, column=0, padx=20, pady=(5,10), sticky="ew")
    discount_frame.grid_columnconfigure(0, weight=1)
    discount_frame.grid_columnconfigure(1, weight=1)

    discount_lumpsum_label = ctk.CTkLabel(discount_frame, text="Discount (Lump Sum):")
    discount_lumpsum_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
    discount_lumpsum_entry = ctk.CTkEntry(discount_frame)
    discount_lumpsum_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    discount_percentage_label = ctk.CTkLabel(discount_frame, text="Discount (%):")
    discount_percentage_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
    discount_percentage_entry = ctk.CTkEntry(discount_frame)
    discount_percentage_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

    apply_discount_button = ctk.CTkButton(discount_frame, text="Apply Discount", command=apply_discount)
    apply_discount_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    discounted_total_label = ctk.CTkLabel(frame_right, text="Discounted Total: £0.00", font=("Arial", 16))
    discounted_total_label.grid(row=6, column=0, padx=20, pady=(5, 10), sticky="e")
    # --------------------- End Discount Section ---------------------

    invoice_list = []  # List to store invoice items

    window.mainloop()

if __name__ == '__main__':
    importdata()
