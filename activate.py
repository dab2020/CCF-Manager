import customtkinter as ctk
from PIL import Image
from CTkMessagebox import CTkMessagebox
from hosuekeeping import makefile
from home import home

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

    # Create the main window
    app = ctk.CTk()
    app.title("CCF Manager")
    app.geometry("1000x500")
    app.iconbitmap('Img/cch.ico')

    # Create a frame for the content
    content_frame = ctk.CTkFrame(app)
    content_frame.pack(expand=True, fill="both")

    # Add the logo (placeholder for now)
    my_image = ctk.CTkImage(light_image=Image.open('Img/cch.png'), dark_image=Image.open('Img/cch.png'), size=(300, 174))
    my_label = ctk.CTkLabel(content_frame, text="", image=my_image)
    my_label.pack(pady=10)

    # Create a frame for the buttons with a fixed height
    button_frame = ctk.CTkFrame(content_frame, height=100)  # Set height for button frame
    button_frame.configure(fg_color="transparent")
    button_frame.pack(side="top", fill="x", pady=10)

    # Style the buttons for larger font and no border
    button_style = ctk.CTkButton(master=app)  # Create a style object
    button_style.configure(width=200, height=200)  # Set width and height for button

    # Adding UI elements
    title = ctk.CTkLabel(button_frame, text="Enter Licence Key")
    title.pack(padx=10, pady=10)

    # Name Input
    name = ctk.StringVar()
    key = ctk.CTkEntry(button_frame, textvariable=name)
    key.pack(padx=10, pady=10)

    button = ctk.CTkButton(button_frame, text="Submit", command=checkkey)
    button.pack()

    # Proper cleanup when closing the app
    def on_closing():
        # Perform any necessary cleanup here
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_closing)

    # Run the application
    app.mainloop()

if __name__ == "__main__":
    activationscreen()
