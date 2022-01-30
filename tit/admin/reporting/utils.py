import shelve
from collections import Counter

from PIL import Image
import base64
from io import BytesIO
import csv

from tit import app

from fpdf import FPDF
from pandas import DataFrame, ExcelWriter

def get_db(database, key, get_x=None, params=None):
    with shelve.open(f"tit/admin/{database}.db", 'c') as db:
        dict = {}
        try:
            dict = db[f'{key}']
        except Exception as ex:
            print(ex)

    if get_x is None:
        return dict
    else:
        datalist = []
        for key in dict:
            obj = dict[key]
            func = getattr(obj, get_x)
            if params is None:
                data = func()
            else:
                data = func(str(params))
            datalist.append(data)
        datalist = Counter(datalist)
        x = []
        y = []
        for xtick in datalist:
            ytick = datalist[xtick]
            if ytick== '':
                ytick = 0
            if xtick=='':
                xtick = 'undefined'
            x.append(xtick)
            y.append(ytick)
        jsondata = {'x': x, 'y': y}
        return jsondata

def set_db(database, key, value):
    with shelve.open(f"tit/admin/{database}.db", 'w') as db:
        db[f'{key}'] = value


def b64toimg(b64str):

    b64str = b64str.replace('data:image/png;base64,', '')
    im = Image.open(BytesIO(base64.b64decode(b64str)))
    im.save('tit/tmp/image.png', 'PNG')

def createPDF(output, imgs):
    WIDTH = 210
    HEIGHT = 297

    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_font('BebasNeue', '', 'BebasNeue-Regular.ttf', uni=True)
    pdf.add_page()
    pdf.image("tit/tmp/Letterhead.png", 0, 0, WIDTH)
    pdf.set_fill_color(255,255,255)
    pdf.rect(5, 50, 100, 50, 'D')
    pdf.set_draw_color(255,255,255)
    pdf.rect(4, 65, 100, 50, 'DF')
    pdf.rect(30, 49, 100, 50, 'DF')

    pdf.set_font('BebasNeue', '', 48)
    pdf.cell(WIDTH-50, 10, "Threads In Time")
    pdf.set_font('BebasNeue', '', 12)
    pdf.cell(0, 0, "Date: 2022/01/24")
    pdf.ln(20)
    pdf.set_font('BebasNeue', '', 32)
    pdf.cell(0, 0, "Report")

    pdf.image("tit/tmp/image.png", 10, 50, WIDTH/2-20)
    pdf.image("tit/tmp/image.png", WIDTH/2+10, 50, WIDTH/2-20)
    #pdf.output(f'{app.config["STATIC_PATH"]}files\\reports\\test.pdf')
    pdf.output(f'{app.config["STATIC_PATH"]}files\\reports\\{output}')
    

def get_ext(x):
    dict = {'1': '.pdf', '2': '.xlsx', "3": '.csv'}
    return dict.get(x)

def create_obj_dict(obj):
    field_dict = {}
    attr_dict = obj.__dict__
    for key in attr_dict:
        field = key.split('__', 1)[1]
        field_dict.update({field:attr_dict[key]})
    return field_dict


def createCSV(output, dict):
    lines = []
    for obj in dict.values():
        lines.append(create_obj_dict(obj))
    fieldnames = lines[0].keys()
    with open(f'{app.config["STATIC_PATH"]}files\\csv\\{output}', 'w', newline='') as csvfile:
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(lines)
    print("csv created")

def createExcel(output, dict_list):
    if not isinstance(dict_list, list):
        dict_list = [dict_list]
    df_list = []
    for dict in dict_list:
        d = {}
        for obj in dict.values():
            obj_dict = create_obj_dict(obj)
            for attr in obj_dict:
                dlist = d.get(attr)
                if dlist is None:
                    dlist = []
                dlist.append(obj_dict.get(attr))
                d.update({attr:dlist})
        df_list.append(DataFrame(data=d))
        df_list.append(DataFrame(data=d))
    with ExcelWriter(f'{app.config["STATIC_PATH"]}files\\excel\\{output}') as writer:  
        for df in df_list:
            df.to_excel(writer, sheet_name='Sheet1')
            df.to_excel(writer, sheet_name='Sheet2')

