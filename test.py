import shelve


with shelve.open('tit/database/users.db', 'r') as db:
    dict = db['Admins']
    print(dict)