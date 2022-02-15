import shelve


with shelve.open('tit/database/users.db', 'r') as db:
    dict = db['Customers'][1].get_cartStatus(0)
    # dict = list(dict.values())[0]['#D849B6737A25'].get_order()s
    print(dict)
