import customtkinter as ctk
from tkinter import ttk
from customerdocgen import generatecustomerinvoice


def importdata():
    # Define validation functions (unchanged from your code)

    def makepdfcustomerinvoice():
        name = first_name_entry.get() + " " + last_name_entry.get()
        phone = phone_entry.get()
        product = invoice_list
        total = 0
        for row in product:
            total += row[3]

        generatecustomerinvoice(name, phone, product, total)

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

    def toggle_room_type_entries(event=None):
        if service_var.get() == "Other":
            room_check.configure(state="disabled")
            livingroom_check.configure(state="disabled")
            hallway_check.configure(state="disabled")
            stairs_check.configure(state="disabled")
            other_check.configure(state="disabled")
            width_entry.configure(state="disabled")
            width_entry.delete(0, "end")
            length_entry.configure(state="disabled")
            length_entry.delete(0, "end")
            num_rooms_entry.configure(state="disabled")
            num_rooms_entry.delete(0, "end")
        else:
            room_check.configure(state="normal")
            livingroom_check.configure(state="normal")
            hallway_check.configure(state="normal")
            stairs_check.configure(state="normal")
            other_check.configure(state="normal")
            if room_var.get() == "Checked":
                width_entry.configure(state="normal")
                length_entry.configure(state="normal")
                num_rooms_entry.configure(state="normal")
            else:
                width_entry.configure(state="disabled")
                length_entry.configure(state="disabled")
                num_rooms_entry.configure(state="disabled")

    def toggle_room_dimensions(event=None):
        if room_var.get() == "Checked":
            width_entry.configure(state="normal")
            length_entry.configure(state="normal")
            num_rooms_entry.configure(state="normal")
        else:
            width_entry.configure(state="disabled")
            length_entry.configure(state="disabled")
            num_rooms_entry.configure(state="disabled")
            width_entry.delete(0, "end")
            length_entry.delete(0, "end")
            num_rooms_entry.delete(0, "end")

    def buttonclick():
        print(invoice_list)

    window = ctk.CTk()
    window.title("Data Entry Form")
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

    frame_left = ctk.CTkFrame(window)
    frame_left.pack(padx=20, pady=10, side="left", fill="both", expand=True)

    frame_right = ctk.CTkFrame(window)
    frame_right.pack(padx=20, pady=10, side="right", fill="both", expand=True)

    user_info_frame = ctk.CTkFrame(frame_left)
    user_info_frame.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="ew")

    first_name_label = ctk.CTkLabel(user_info_frame, text="First Name")
    first_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    last_name_label = ctk.CTkLabel(user_info_frame, text="Last Name")
    last_name_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    first_name_entry = ctk.CTkEntry(user_info_frame)
    last_name_entry = ctk.CTkEntry(user_info_frame)
    first_name_entry.grid(row=1, column=0, padx=10, pady=5)
    last_name_entry.grid(row=1, column=1, padx=10, pady=5)

    phone_label = ctk.CTkLabel(user_info_frame, text="Phone Number")
    phone_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    phone_entry = ctk.CTkEntry(user_info_frame)
    phone_entry.grid(row=3, column=0, padx=10, pady=5)

    address_label = ctk.CTkLabel(user_info_frame, text="Address")
    address_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    address_entry = ctk.CTkEntry(user_info_frame)
    address_entry.grid(row=3, column=1, padx=10, pady=5)

    parking_label = ctk.CTkLabel(user_info_frame, text="Parking")
    parking_combobox = ctk.CTkComboBox(user_info_frame, values=["Driveway", "Onstreet", "Paid", "No Parking"])
    parking_label.grid(row=2, column=2, padx=10, pady=5, sticky="w")
    parking_combobox.grid(row=3, column=2, padx=10, pady=5)

    service_frame = ctk.CTkFrame(frame_left)
    service_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

    service_label = ctk.CTkLabel(service_frame, text="Type of Service")
    service_var = ctk.StringVar(value="Carpet")
    service_combobox = ctk.CTkComboBox(service_frame, values=["Carpet", "Laminate", "Wood", "Vinyl tile", "Other"],
                                       variable=service_var, command=lambda _: toggle_room_type_entries())
    service_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    service_combobox.grid(row=1, column=0, padx=10, pady=5)

    room_var = ctk.StringVar(value="Not Checked")
    room_check = ctk.CTkCheckBox(service_frame, text="Room", variable=room_var, onvalue="Checked",
                                 offvalue="Not Checked",
                                 command=toggle_room_dimensions)
    room_check.grid(row=2, column=0, padx=10, pady=5, sticky="w")

    livingroom_var = ctk.StringVar(value="Not Checked")
    livingroom_check = ctk.CTkCheckBox(service_frame, text="Living Room", variable=livingroom_var, onvalue="Checked",
                                       offvalue="Not Checked")
    livingroom_check.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    hallway_var = ctk.StringVar(value="Not Checked")
    hallway_check = ctk.CTkCheckBox(service_frame, text="Hallway", variable=hallway_var, onvalue="Checked",
                                    offvalue="Not Checked")
    hallway_check.grid(row=2, column=2, padx=10, pady=5, sticky="w")

    stairs_var = ctk.StringVar(value="Not Checked")
    stairs_check = ctk.CTkCheckBox(service_frame, text="Stairs", variable=stairs_var, onvalue="Checked",
                                   offvalue="Not Checked")
    stairs_check.grid(row=3, column=0, padx=10, pady=5, sticky="w")

    other_var = ctk.StringVar(value="Not Checked")
    other_check = ctk.CTkCheckBox(service_frame, text="Other", variable=other_var, onvalue="Checked",
                                  offvalue="Not Checked")
    other_check.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    dimensions_frame = ctk.CTkFrame(frame_left)
    dimensions_frame.grid(row=2, column=0, padx=20, pady=(5, 10), sticky="ew")

    width_label = ctk.CTkLabel(dimensions_frame, text="Width (m)")
    width_entry = ctk.CTkEntry(dimensions_frame, validate="key",
                               validatecommand=(window.register(validate_float), '%P'))
    width_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    width_entry.grid(row=1, column=0, padx=10, pady=5)
    width_entry.configure(state="disabled")

    length_label = ctk.CTkLabel(dimensions_frame, text="Length (m)")
    length_entry = ctk.CTkEntry(dimensions_frame, validate="key",
                                validatecommand=(window.register(validate_float), '%P'))
    length_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    length_entry.grid(row=1, column=1, padx=10, pady=5)
    length_entry.configure(state="disabled")

    num_rooms_label = ctk.CTkLabel(dimensions_frame, text="Number of Rooms")
    num_rooms_entry = ctk.CTkEntry(dimensions_frame, validate="key",
                                   validatecommand=(window.register(validate_integer), '%P'))
    num_rooms_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")
    num_rooms_entry.grid(row=1, column=2, padx=10, pady=5)
    num_rooms_entry.configure(state="disabled")

    other_info_label = ctk.CTkLabel(frame_left, text="Other Information")
    other_info_label.grid(row=3, column=0, padx=10, pady=(10, 5), sticky="w")
    other_info_textbox = ctk.CTkTextbox(frame_left, width=200, height=100)
    other_info_textbox.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

    carpet_info_frame = ctk.CTkFrame(frame_right)
    carpet_info_frame.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="ew")

    carpet_name_label = ctk.CTkLabel(carpet_info_frame, text="Carpet Name")
    carpet_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    carpet_name_entry = ctk.CTkEntry(carpet_info_frame)
    carpet_name_entry.grid(row=1, column=0, padx=10, pady=5)

    underlay_label = ctk.CTkLabel(carpet_info_frame, text="Underlay")
    underlay_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    underlay_entry = ctk.CTkEntry(carpet_info_frame)
    underlay_entry.grid(row=1, column=1, padx=10, pady=5)

    grippers_label = ctk.CTkLabel(carpet_info_frame, text="Grippers")
    grippers_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")
    grippers_entry = ctk.CTkEntry(carpet_info_frame)
    grippers_entry.grid(row=1, column=2, padx=10, pady=5)

    door_bars_label = ctk.CTkLabel(carpet_info_frame, text="Door Bars")
    door_bars_combobox = ctk.CTkComboBox(carpet_info_frame, values=["Silver", "Gold", "Special"])
    door_bars_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    door_bars_combobox.grid(row=3, column=0, padx=10, pady=5)

    door_bars_type_label = ctk.CTkLabel(carpet_info_frame, text="Door Bars Type")
    door_bars_type_combobox = ctk.CTkComboBox(carpet_info_frame, values=["Double", "Single", "Zbar", "Flet", "Other"])
    door_bars_type_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    door_bars_type_combobox.grid(row=3, column=1, padx=10, pady=5)

    uplift_var = ctk.StringVar(value="Not Checked")
    uplift_check = ctk.CTkCheckBox(carpet_info_frame, text="Uplift", variable=uplift_var, onvalue="Checked",
                                   offvalue="Not Checked")
    uplift_check.grid(row=4, column=0, padx=10, pady=5, sticky="w")

    dispose_var = ctk.StringVar(value="Not Checked")
    dispose_check = ctk.CTkCheckBox(carpet_info_frame, text="Dispose", variable=dispose_var, onvalue="Checked",
                                    offvalue="Not Checked")
    dispose_check.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    empty_var = ctk.StringVar(value="Not Checked")
    empty_check = ctk.CTkCheckBox(carpet_info_frame, text="Empty", variable=empty_var, onvalue="Checked",
                                  offvalue="Not Checked")
    empty_check.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    new_button2 = ctk.CTkButton(carpet_info_frame, text="Generate Customer Invoice", command=makepdfcustomerinvoice)
    new_button2.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

    new_button = ctk.CTkButton(carpet_info_frame, text="Generate Installer Copy")
    new_button.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

    item_info_frame = ctk.CTkFrame(frame_right)
    item_info_frame.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="ew")

    qty_label = ctk.CTkLabel(item_info_frame, text="Qty")
    qty_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    qty_spinbox = ctk.CTkEntry(item_info_frame, validate="key",
                               validatecommand=(window.register(validate_integer), '%P'))
    qty_spinbox.grid(row=1, column=0, padx=10, pady=5)

    desc_label = ctk.CTkLabel(item_info_frame, text="Name of Product")
    desc_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    desc_entry = ctk.CTkEntry(item_info_frame)
    desc_entry.grid(row=1, column=1, padx=10, pady=5)

    price_label = ctk.CTkLabel(item_info_frame, text="Unit Price")
    price_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")
    price_spinbox = ctk.CTkEntry(item_info_frame, validate="key",
                                 validatecommand=(window.register(validate_float), '%P'))
    price_spinbox.grid(row=1, column=2, padx=10, pady=5)

    add_item_button = ctk.CTkButton(item_info_frame, text="Add item",
                                    command=lambda: add_item(tree, qty_spinbox, desc_entry, price_spinbox))
    add_item_button.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

    columns = ('qty', 'desc', 'price', 'total')
    tree = ttk.Treeview(frame_right, columns=columns, show="headings", style="Treeview")
    tree.heading('qty', text='Qty')
    tree.heading('desc', text='Name of Product')
    tree.heading('price', text='Unit Price')
    tree.heading('total', text='Total')

    tree.column('qty', width=50)
    tree.column('desc', width=200)
    tree.column('price', width=50)
    tree.column('total', width=50)

    tree.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

    invoice_list = []

    def clear_item():
        qty_spinbox.delete(0, ctk.END)
        qty_spinbox.insert(0, "1")
        desc_entry.delete(0, ctk.END)
        price_spinbox.delete(0, ctk.END)
        price_spinbox.insert(0, "0.0")

    def add_item(tree, qty_spinbox, desc_entry, price_spinbox):
        qty = int(qty_spinbox.get())
        desc = desc_entry.get()
        price = float(price_spinbox.get())
        line_total = qty * price
        invoice_item = [qty, desc, price, line_total]
        tree.insert('', 0, values=invoice_item)
        clear_item()
        invoice_list.append(invoice_item)

    toggle_room_type_entries()
    window.mainloop()
