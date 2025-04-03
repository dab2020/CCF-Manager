import customtkinter as ctk
from PIL import Image
from CTkMessagebox import CTkMessagebox
from housekeeping import makefile
from home import home
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def activationscreen():
    def checkkey():
        value = key.get()
        if value.lower() == "fbkgcplhde":
            makefile()
            app.destroy()
            home()
        else:
            CTkMessagebox(title="Information", message="Invalid Licence Key, Please Try Again")

    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("green")

    app = ctk.CTk()
    app.title("CCF Manager")
    app.geometry("1000x500")

    content_frame = ctk.CTkFrame(app)
    content_frame.pack(expand=True, fill="both")

    my_image = ctk.CTkImage(light_image=Image.open(resource_path('Img/cch.png')),
                            dark_image=Image.open(resource_path('Img/cch.png')),
                            size=(300, 174))
    my_label = ctk.CTkLabel(content_frame, text="", image=my_image)
    my_label.pack(pady=10)

    button_frame = ctk.CTkFrame(content_frame, height=100)
    button_frame.configure(fg_color="transparent")
    button_frame.pack(side="top", fill="x", pady=10)

    button_style = ctk.CTkButton(master=app)
    button_style.configure(width=200, height=200)

    title = ctk.CTkLabel(button_frame, text="Enter Licence Key")
    title.pack(padx=10, pady=10)

    name = ctk.StringVar()
    key = ctk.CTkEntry(button_frame, textvariable=name)
    key.pack(padx=10, pady=10)

    button = ctk.CTkButton(button_frame, text="Submit", command=checkkey)
    button.pack()

    def on_closing():
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()

if __name__ == "__main__":
    activationscreen()
