from flask import request

import shelve
from collections import Counter

from tit.classes.Notification import Notification


def parseVisitor(data, session_id):
    sessions_dict = get_db('traffic', 'Sessions')
    viewer = sessions_dict.get(session_id)
    if viewer is None:
        return 'Session ID does not exist'
    viewer.update_views(data)
    sessions_dict[session_id] = viewer
    set_db('traffic', 'Sessions', sessions_dict)
    return f'{session_id} Parsed'

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
