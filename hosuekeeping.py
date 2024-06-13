import shutil
import os
import os.path


def cleanup():
    folder_path = os.path.join('dependencies', 'sumatrapdfcache')
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.remove("dependencies/SumatraPDF-settings.txt")


def checkactivation():
    file_path = 'version.txt'

    if os.path.exists(file_path):
        return True
    else:
        return False


def makefile():
    with open("version.txt", 'w') as file:
        file.write("Developed by Syndicate Solutions\n")
        file.write("Version 1.0")
