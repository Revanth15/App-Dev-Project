from flask import request
from os import listdir

import shelve
import json

from tit.classes.Notification import Notification


def dbkeys(flag=False):
        
    mypath = 'tit/database'
    db_dict = {}
    for f in listdir(mypath):
        if f.endswith('.dat'):
            f=f.rstrip('.dat')
            db = shelve.open(f'tit/database/{f}', 'c')
            klist = list(db.keys())
            db_dict.update({f: klist})
            db.close()
    if flag :
        print(db_dict)
    return db_dict
                
def get_db(database, key, v=None):
    if v is None:
        default = {}
    else:
        default = v
    if '.db' in database:
        print('".db" found in argument! If this was not intentional, please remove it as .db is appended automatically.')
    if database+'.db' not in dbkeys().keys():
        print('Database not found! Returning empty dictionary')
        return default
    db = shelve.open(f"tit/database/{database}.db", 'r')
    default_value = default
    try:
        default_value = db[str(key)]
        print(f'Retrieved {database}[{key}] Successfully!')

    except KeyError:
        print(f'Error Retrieving {database}[{key}]')
        print(f'Key [{key}] not found')
        print(f'Returning {default_value}')

    except Exception as ex:
        print(ex)
    db.close()

    return default_value
    
def set_db(database, key, value):
    if '.db' in database:
        print('".db" found in argument! If this was not intentional, please remove it as .db is appended automatically.')
    if database+'.db' not in dbkeys().keys():
        print('Database not found! Creating new database')
    db = shelve.open(f"tit/database/{database}.db", 'c')
    db[f'{key}'] = value
    print(f'Set value for {database}[{key}] Successfully!')
    db.close()

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
    file = open('index.json', 'r')
    index = json.load(file)
    file.close()
    
    path = request.path
    method = request.method
    
    if index.get(path) is not None:
        if index.get(path).get(method) is not None and index.get(path).get(method) != '':
            return index.get(path).get(method)
        else:
            return "Unnamed Event"
    else:
        return "Path not registered"
        
# def update_url_map():
#     file = open('index.txt', 'r')
#     index = file.read()
#     file.close()
#     index = json.loads(index)
#     if request.method == 'POST':
#         for rule in app.url_map.iter_rules():
#             if rule.__str__() not in index:
#                 rule_dict = {}
#                 for method in rule.methods:
#                     if method == 'GET':
#                         rule_dict.update({method:'view'})
#                     elif method == 'POST':
#                         rule_dict.update({method:''})
#                 index.update({rule.__str__():rule_dict})