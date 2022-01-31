from traceback import print_tb
from flask import request

import shelve
from collections import Counter


def parseVisitor(data, session_id):
    sessions_dict = get_db('traffic', 'Sessions')
    viewer = sessions_dict.get(session_id)
    viewer.update_views(data)
    sessions_dict[session_id] = viewer
    set_db('traffic', 'Sessions', sessions_dict)
    return session_id

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