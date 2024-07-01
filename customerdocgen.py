import os
from datetime import date
from docx2pdf import convert
from docxtpl import DocxTemplate
import subprocess
import sys


# def resource_path(relative_path):
#    """ Get absolute path to resource, works for dev and for PyInstaller """
#    try:
#        base_path = sys._MEIPASS
#   except Exception:
#        base_path = os.path.abspath(".")
#   return os.path.join(base_path, relative_path)

def generatecustomerinvoice(name, phone, product, total, paymeth):
    doc = DocxTemplate('invoice_template.docx')
    today = date.today().strftime('%B %d, %Y')
    filename = "invoice/" + str(date.today()) + " " + name + "customer.docx"
    filepdf = "invoice/" + str(date.today()) + " " + name + "customer.pdf"
    doc.render(
        {"name": name, "invoice_list": product, "phone": phone, "total": total, "date": today, "paymeth": paymeth})
    doc.save(filename)
    cont2pdf(filename)
    deldocx(filename)
    printf(filepdf)


def cont2pdf(name):
    convert(name)


def deldocx(name):
    if os.path.exists(name):
        os.remove(name)


def printf(name):
    current_working_directory = os.getcwd()
    pathtodllhost = os.path.join("dependencies", "dllhostpdf.exe")
    subprocess.Popen([pathtodllhost, "-print-dialog", name], shell=True)


def generateinstall(name, phone, product, parking, zipcode, room, installname1, address1, deldate2, fitdate2, otherin):
    doc = DocxTemplate('installer_template.docx')
    today = date.today().strftime('%B %d, %Y')
    filename = "invoice/" + str(date.today()) + " " + name + "installer.docx"
    filepdf = "invoice/" + str(date.today()) + " " + name + "installer.pdf"
    context = {
        "name": name, "invoice_list": product, "phone": phone, "date": today,
        "parking": parking, "room_list": room, "installname": installname1, "zipcode": zipcode,
        "add": address1, "deldate": deldate2, "fittingdate": fitdate2, "otherinfo": otherin
    }
    doc.render(context)
    doc.save(filename)
    cont2pdf(filename)
    deldocx(filename)
    printf(filepdf)
