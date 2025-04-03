import os

os.environ["TQDM_DISABLE"] = "1"
from datetime import date
from docx2pdf import convert
from docxtpl import DocxTemplate
import subprocess
import traceback
from tqdm import tqdm


class SilentTqdm(tqdm):
    def __init__(self, *args, **kwargs):
        # Initialize the parent class with a file-like object that does nothing
        super().__init__(*args, **kwargs, file=open(os.devnull, 'w'))

    def display(self, **kwargs):
        pass

    def refresh(self, **kwargs):
        pass


def generatecustomerinvoice(name, phone, product, total, paymeth, vetflag, depflag, uniqueid, zipcode, address1, dayyan):
    totalwd = int(total) - int(dayyan)
    if vetflag:
        totalwtax = 1.2 * int(totalwd)
        vet = 0.2 * int(totalwd)
        vet = round(vet, 2)
        totalwtax = round(totalwtax, 2)
    else:
        totalwtax = totalwd
        vet = 0

    if depflag:
        left = 0.5 * int(totalwtax)
        advance = 0.5 * int(totalwtax)
    else:
        left = totalwtax
        advance = 0
    doc = DocxTemplate('invoice_template.docx')
    today = date.today().strftime('%B %d, %Y')
    filename = "invoice/" + str(date.today()) + " " + name + "customer.docx"
    filepdf = "invoice/" + str(date.today()) + " " + name + "customer.pdf"
    doc.render(
        {"name": name, "invoice_list": product, "phone": phone, "total": total, "date": today, "paymeth": paymeth,
         "vet": vet, "left": left, "advance": advance, "totalwtax": totalwtax, "uid": uniqueid, "zipcode": zipcode,
         "add": address1, "dayyan": dayyan})
    doc.save(filename)
    cont2pdf(filename)
    deldocx(filename)
    printf(filepdf)


def cont2pdf(name):
    log_path = os.path.abspath("error_log.txt")
    try:
        # Use the custom silent progress bar with docx2pdf
        with SilentTqdm(total=1):
            convert(name)
    except Exception as e:
        # Log errors to a file with robust error handling
        try:
            with open(log_path, "w") as f:
                f.write("An error occurred:\n")
                f.write(str(e) + "\n")
                f.write(traceback.format_exc() + "\n")
        except Exception as log_error:
            print(f"Failed to write to log file: {log_error}")


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
