import shutil
import os
from database import initialize_database
import sys


def incvalue(filename='crmpwd.txt'):
    try:
        # Try to open the file in read mode
        with open(filename, 'r') as file:
            value = int(file.read().strip())
    except FileNotFoundError:
        # If the file does not exist, start with the value 1
        value = 0

    # Increment the value by 1
    value += 1

    # Write the updated value back to the file
    with open(filename, 'w') as file:
        file.write(str(value))

    # Return the updated value
    return value


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def cleanup():
    folder_path = resource_path(os.path.join('dependencies', 'sumatrapdfcache'))
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.remove(resource_path("dependencies/SumatraPDF-settings.txt"))


def checkactivation():
    file_path = resource_path('version.txt')

    if os.path.exists(file_path):
        return True
    else:
        return False


def makefile():
    with open(resource_path("version.txt"), 'w') as file:
        file.write("Developed by Syndicate Solutions\n")
        file.write("Version 1.0")
    initialize_database()
