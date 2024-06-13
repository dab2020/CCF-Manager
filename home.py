import customtkinter as ctk
from tkinter import *
from PIL import Image
from enter import importdata


def home():
    def gotodataentryscreen():
        importdata()

    # System Settings
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("green")

    # Create the main window
    root = ctk.CTk()
    root.title("CCF Manager")
    root.geometry("1000x500")
    root.iconbitmap('Img/cch.ico')
    # Create a frame for the content
    content_frame = ctk.CTkFrame(root)
    content_frame.pack(expand=True, fill="both")

    # Add the logo (placeholder for now)
    my_image = ctk.CTkImage(light_image=Image.open('Img/cch.png'), dark_image=Image.open('Img/cch.png'),
                            size=(300, 174))
    my_label = ctk.CTkLabel(content_frame, text="", image=my_image)
    my_label.pack(pady=10)

    # Create a frame for the buttons with a fixed height
    button_frame = ctk.CTkFrame(content_frame, height=100)
    button_frame.configure(fg_color="transparent")
    button_frame.pack(side="top", fill="x", pady=100)

    # Style the buttons for larger font and no border
    button_style = ctk.CTkButton(master=root)
    button_style.configure(width=200, height=40)

    # Add the "Add a new sale" button with the defined font
    add_sale_button = ctk.CTkButton(button_frame, text="Add a new sale", font=("Arial", 18), width=200, height=40,
                                    border_width=0, command=gotodataentryscreen)
    add_sale_button.pack(side="left", padx=100)

    # Add the "View old sale" button with the defined font
    view_sale_button = ctk.CTkButton(button_frame, text="View old sale", font=("Arial", 18), width=200, height=40,
                                     border_width=0)
    view_sale_button.pack(side="right", padx=100)

    # Run the application
    root.mainloop()
