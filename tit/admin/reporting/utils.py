import os
from PIL import Image
import base64
from io import BytesIO
import csv
from collections import Counter
from os import listdir
from tit import app

from fpdf import FPDF
from pandas import DataFrame, ExcelWriter
from tit.utils import get_db

def db_count_occurence(database, dbkey, method, args=None):
    dict = get_db(database, dbkey)

    datalist= []
    for key in dict:
        obj = dict[key]
        func = getattr(obj, method)
        if args is None:
            data = func()
        else:
            data = func(str(args))
        datalist.append(data)
    datalist = Counter(datalist)
    x = []
    y = []
    for xtick in datalist:
        ytick = datalist[xtick]
        if ytick== '' or None:
            ytick = 0
        if xtick=='':
            xtick = 'undefined'
        x.append(xtick)
        y.append(ytick)
    jsondata = {'x': x, 'y': y}
    return jsondata

def db_get_qty(database, dbkey, method, args=None):
    dict = get_db(database, dbkey)

    x = []
    y = []
    for key in dict:
        obj = dict[key]
        func = getattr(obj, method)
        if args is None:
            data = func()
        else:
            data = func(str(args))
        if data == '' or None:
            data = 0
        if str(obj) == '':
            obj = 'undefined'
        x.append(str(obj))
        y.append(data)
    jsondata = {'x': x, 'y': y}
    return jsondata

def b64toimg(b64strs):
    b64strs = b64strs.split(',')
    index = 0
    for string in b64strs:
        if not string.startswith('data') and string != '':
            imgdata = base64.b64decode(str(string))
            im = Image.open(BytesIO(imgdata))    
            im.save(f'tit/tmp/chart{index}.png', 'PNG')
            index += 1

def createPDF(output, imgs, choices):
    print(choices)
    WIDTH = 210
    HEIGHT = 297

    b64toimg(imgs)

    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_font('BebasNeue', '', 'BebasNeue-Regular.ttf', uni=True)
    pdf.add_page()
    
    pdf.image(f"{app.config['STATIC_PATH']}/images/Letterhead.png", 0, 0, WIDTH)
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

    index = 0
    height = 50
    for img in listdir('tit/tmp'):
        if int(img[-5]) in choices:
            print('img!')
            if index % 2 == 0:
                pdf.image(f"tit/tmp/{img}", 10, height, WIDTH/2-20)
            else:
                pdf.image(f"tit/tmp/{img}", WIDTH/2+10, height, WIDTH/2-20)
                height+=50
            index +=1
        os.remove(img)
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

