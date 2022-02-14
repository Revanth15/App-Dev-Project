import shelve


with shelve.open('tit/database/orders.db', 'r') as db:
    dict = db['orders']
    dict = list(dict.values())[0]['#D849B6737A25'].get_order()
    print(dict)