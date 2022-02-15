import datetime
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
from tit.utils import get_db, current_time

def db_add_manual(dict):
    x = []
    y = []
    for key in dict:
        x.append(key)
        y.append(dict[key])
    jsondata = {'x': x, 'y': y}
    return jsondata



def db_count_occurence(datalist):
    datalist = Counter(datalist)
    x = []
    y = []
    for xtick in datalist:
        ytick = datalist[xtick]
        if ytick== ('' or None or []):
            ytick = 0
        if xtick=='':
            xtick = 'undefined'
        x.append(xtick)
        y.append(ytick)
    jsondata = {'x': x, 'y': y}
    return jsondata

def db_get_qty(database, dbkey, method, args=None):
    dict = get_db(database, dbkey)
    if len(dict) == 0:
        return {}
    x = []
    y = []
    for key in dict:
        obj = dict[key]
        func = getattr(obj, method)
        if args is None:
            data = func()
        else:
            data = func(str(args))

        if data == ('' or None or []):
            data = 0
        if str(obj) == '':
            obj = 'undefined'
        x.append(str(obj))
        y.append(data)
    jsondata = {'x': x, 'y': y}
    return jsondata

def get_data():
    data = []
    datalist = []
    restock_db = get_db('products','delivery')
    for restock in restock_db.values():
        if restock.get_created('date', 'obj') == current_time().date():
            datalist.append(restock.get_sku())
    data.append(db_count_occurence(datalist))

    datalist = []
    stock_db = get_db('notification','Notifications')
    for stock in stock_db.values():
        if stock.get_created(flag='obj').year == current_time().year and stock.get_type() == 'LS':
            datalist.append(stock.get_obj_id())
    data.append(db_count_occurence(datalist))


    datalist = []
    stock_db = get_db('notification','Notifications')
    for stock in stock_db.values():
        if stock.get_created(flag='obj').year == current_time().year and stock.get_type() == 'OOS':
            datalist.append(stock.get_obj_id())
    data.append(db_count_occurence(datalist))


    data.append(db_get_qty('products', 'products', 'get_quantity'))


    order_db = get_db('orders','orders')
    revenue_dict = {}
    for user in order_db.values():
        for order in user.values():
            if order.get_created(flag='obj').year == current_time().year:
                total = 0 if revenue_dict.get(order.get_created('%Y-%m')) is None else revenue_dict.get(order.get_created('%Y-%m'))
                total += order.get_total_price()
                revenue_dict[order.get_created('%Y-%m')] = total
    data.append(db_add_manual(revenue_dict))

    datalist = []
    for user in order_db.values():
        for order in user.values():
            if order.get_created(flag='obj').year == current_time().year:
                datalist.append(order.get_created('%m-%d'))
    data.append(db_count_occurence(datalist))


    datalist = []
    session_db = get_db('traffic','Sessions')
    for session in session_db.values():
        
        if session.get_views()[-1][1].date() == current_time().date():
            datalist.append(session.get_created('%I%p'))
    data.append(db_count_occurence(datalist))

    datalist = []
    user_db = get_db('users', 'Customers')
    for user in user_db.values():
        print(user.get_cartStatus(0))
        datalist.append(user.get_cartStatus(0))
    data.append(db_count_occurence(datalist))

    print(data)
    return data

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
        if os.path.exists('tit\\tmp'+img):
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

