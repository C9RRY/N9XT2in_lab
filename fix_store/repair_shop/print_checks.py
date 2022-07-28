import openpyxl
from openpyxl import load_workbook
import textwrap
import qrcode
from pathlib import Path


static_path = Path(__file__).resolve().parent.parent


def create_qr(url):
    qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=4, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    image = qr.make_image()
    image.save(f"{static_path}/media/img/client.png")


def paste_to_order(data):
    model, package, breakage, name, phone_num, date, slug =\
        data[2], data[3], data[4], data[5], data[6], data[7], data[9]
    url = f'http://172.20.10.8:8000/client_card/{slug}/'
    create_qr(url)
    wb = load_workbook(f"{static_path}/media/excel_files/examples/order.xlsx")
    ws = wb.worksheets[0]
    img = openpyxl.drawing.image.Image(f"{static_path}/media/img/client.png")
    img.anchor = 'K11'
    ws.add_image(img)
    short_date = date.strftime("%d.%m.%Y")
    longest_date = date.strftime("%d.%m.%Y %H:%M")
    string_width = 25
    ws["C10"], ws["L10"], ws["C11"], ws["L11"], ws["C13"], ws["L13"], ws["C14"] =\
        model, model, package, package, name, name, phone_num
    ws["C17"], ws["M18"] = short_date, short_date
    breakage = textwrap.fill(breakage, string_width).split("\n")
    ws["C12"], ws["L12"] = breakage[0], breakage[0]
    wb.save(f"{static_path}/media/excel_files/sawed_xlsx/{name}_{longest_date}.xlsx")
    return f'media/excel_files/sawed_xlsx/{name}_{longest_date}.xlsx'


def paste_to_warranty(client_id, break_fix, date, price, warranty):
    wb = load_workbook(f"{static_path}/media/excel_files/examples/warranty.xlsx")
    ws = wb.worksheets[0]
    short_date = date.strftime("%d.%m.%Y")
    string_width = 30
    ws["d10"] = client_id
    break_fix = textwrap.fill(break_fix, string_width).split("\n")
    ws["A11"] = break_fix[0]
    if len(break_fix) > 1:
        ws["A12"] = break_fix[1]
    else:
        ws["A12"] = ""
    if len(break_fix) > 2:
        ws["A13"] = break_fix[2]
    else:
        ws["A13"] = ""
    ws["B14"] = warranty
    ws["C15"] = price + ".00грн."
    ws["B16"] = short_date
    wb.save(f"{static_path}/media/excel_files/examples/warranty.xlsx")


if __name__ == '__main__':
    print(Path(__file__).resolve().parent)
