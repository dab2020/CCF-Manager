import os
from datetime import date
from docx2pdf import convert
from docxtpl import DocxTemplate
import subprocess


def generatecustomerinvoice(name, phone, product, total):
    doc = DocxTemplate('invoice_template.docx')
    today = date.today().strftime('%B %d, %Y')
    filename = "customercopy/" + str(date.today()) + " " + name + ".docx"
    filepdf = "customercopy/" + str(date.today()) + " " + name + ".pdf"
    doc.render(
        {"name": name, "invoice_list": product, "phone": phone, "total": total,
         "date": today})
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
    pathtodllhost = current_working_directory + "/dependencies/dllhostpdf.exe"
    pathtodllhost = os.path.normpath(pathtodllhost)
    subprocess.Popen([pathtodllhost, "-print-dialog", name])
