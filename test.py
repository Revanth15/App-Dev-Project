import shelve


with shelve.open('tit/database/vouchers.db', 'r') as db:
    dict = db['Vouchers']
    print(dict)