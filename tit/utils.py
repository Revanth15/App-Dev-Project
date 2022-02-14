from flask import request

import shelve
import ast
import json

from tit import app
from collections import Counter

from tit.classes.Notification import Notification



def get_ip():
    return request.remote_addr

def get_db(database, key, get_x=None, params=None):
    with shelve.open(f"tit/database/{database}.db", 'c') as db:
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
    with shelve.open(f"tit/database/{database}.db", 'w') as db:
        db[f'{key}'] = value

def get_notifications(id=None):
    notification_dict = get_db('notification', 'Notifications')
    if id is None:
        return notification_dict
    return notification_dict.get(id)

def set_notifications(name, type, message, url):
    notification_dict = get_db('notification', 'Notifications')
    notification = Notification(name, type, message, url)
    notification_dict[notification.get_id()] = notification
    set_db('notification', 'Notifications', notification_dict)

def event():
    file = open('index.txt', 'r')
    index = file.read()
    index = json.loads(index)
    file.close()
    print(index)
    
    # path = request.path
    # method = request.method
    # index = app.url
    # if path == '/' and 
        
def update_url_map():
    file = open('index.txt', 'r')
    index = file.read()
    file.close()
    index = json.loads(index)
    if request.method == 'POST':
        for rule in app.url_map.iter_rules():
            if rule.__str__() not in index:
                rule_dict = {}
                for method in rule.methods:
                    if method == 'GET':
                        rule_dict.update({method:'view'})
                    elif method == 'POST':
                        rule_dict.update({method:''})
                index.update({rule.__str__():rule_dict})