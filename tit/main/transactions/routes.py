from io import SEEK_CUR
from flask import render_template, request, redirect, url_for, Blueprint
import shelve
from tit import app 

transactions = Blueprint('transactions', __name__, template_folder='templates', static_url_path='static', url_prefix='/transactions')

@transactions.route('/cart', methods=['GET','POST'])
def cart(): 
    user_id = 1
    if request.method == 'POST':
        with shelve.open('tit/database/cart.db','c') as cart_db:
            cart_dict = {}
            try:
                cart_dict = cart_db['cart']
            except:
                print("Error in retrieving Items from cart.db")
            sku = int(request.form['sku'])
            if cart_dict.get(user_id) is None:
                cart_dict[user_id] = {}
                
            if sku in cart_dict.get(user_id):
                cart_dict[user_id][sku] = cart_dict[user_id][sku] + 1
            else:
                cart_dict[user_id].update({sku: 1})

            cart_db['cart'] = cart_dict
    with shelve.open('tit/database/cart.db','c') as cart_db: 
        with shelve.open('tit/database/products.db','r') as db:
            cart_dict = {}
            product_dict = {}
            try:
                cart_dict = cart_db['cart']
            except:
                print("Error in retrieving Items from cart.db")
            try:
                product_dict = db['products']
            except:
                print("Error in retrieving Products from products.db")
            user_cart = cart_dict.get(user_id)
            if user_cart is None:
                user_cart = {}
            cart_list = []
            for sku in user_cart:
                if str(sku) in product_dict:
                    product = product_dict.get(str(sku))
                    cart_list.append([product,user_cart[sku]])

    return render_template('inventory/cart.html', cart_list = cart_list)


@transactions.route('/remove_item/<sku>', methods=['POST'])
def remove_item(sku):
    print(sku)
    user_id = 1
    cart_dict = {}
    cart_db = shelve.open('tit/database/cart.db', 'w')
    cart_dict = cart_db['cart']
    print(cart_dict[user_id])
    cart_dict[user_id].pop(int(sku))

    cart_db['cart'] = cart_dict
    cart_db.close() 

    return redirect(url_for('main.transactions.cart'))

@transactions.route('/delete_cart/<user_id>', methods=['POST'])
def delete_cart(user_id):
    cart_dict = {}
    cart_db = shelve.open('tit/database/cart.db', 'w')
    cart_dict = cart_db['cart']
    print(cart_dict)
    cart_dict.pop(int(user_id))
    print(cart_dict)

    cart_db['cart'] = cart_dict
    cart_db.close() 

    return redirect(url_for('main.transactions.cart'))

@transactions.route('/update_cart' ,methods=['GET'])
def update_cart():
    with shelve.open('tit/database/cart.db','c') as cart_db: 
        user_id = 1
        cart_dict = {}
        try:
            cart_dict = cart_db['cart']
        except:
            print("Error in retrieving Items from cart.db")
        sku = int(request.args.get('sku'))
        quantity = int(request.args.get('quantity'))
        if int(quantity) <= 0:
            quantity = 1
        cart_dict[user_id].update({sku: quantity})
        cart_db['cart'] = cart_dict
    return '1'

# def cart(): 
#     user_id = 1
#     if request.method == 'POST':
#         with shelve.open('cart.db','c') as cart_db:
#             with shelve.open('products.db','r') as product_db:
#                 cart_dict = {}
#                 product_dict = {}
#                 try:
#                     cart_dict = cart_db['cart']
#                 except:
#                     print("Error in retrieving Items from cart.db")
#                 try:
#                     product_dict = product_db['products']
#                 except:
#                     print("Error in retrieving Products from products.db")
#                 cart_list = cart_dict.get(user_id)
#                 if cart_list is None:
#                     cart_list = []
#                 sku = (request.form['sku'])
#                 product = product_dict.get(sku)
#                 cart_list.append(product)
#                 cart_dict[user_id] = cart_list
#                 cart_db['cart'] = cart_dict
#     with shelve.open('cart.db','c') as cart_db: 
#         cart_dict = {}
#         try:
#             cart_dict = cart_db['cart']
#         except:
#             print("Error in retrieving Items from cart.db")
#         cart_list = cart_dict.get(user_id)
#         if cart_list is None:
#             cart_list = []
#     return render_template('cart.html', cart_list = cart_list)

# def remove_cart(sku):
#     user_id = 1
#     cart_dict = {}
#     cart_db = shelve.open('cart.db', 'w')
#     cart_dict = cart_db['cart']
#     cart_dict[user_id].pop(int(sku))

#     cart_db['products'] = cart_dict
#     cart_db.close() 

#     return redirect(url_for('main.transactions.cart'))

# @transactions.route('/cart', methods=['GET','POST'])
# def cart(): 
#     user_id = 1
#     if request.method == 'POST':
#         with shelve.open('cart.db','c') as cart_db:
#             with shelve.open('products.db','r') as product_db:
#                 cart_dict = {}
#                 product_dict = {}
#                 try:
#                     cart_dict = cart_db['cart']
#                 except:
#                     print("Error in retrieving Items from cart.db")
#                 try:
#                     product_dict = product_db['products']
#                 except:
#                     print("Error in retrieving Products from products.db")
#                 cart_list = cart_dict.get(user_id)
#                 if cart_list is None:
#                     cart_list = []
#                 sku = int(request.form['sku'])
#                 product = product_dict.get(sku)
#                 cart_list.append(sku)
#                 cart_dict[user_id] = cart_list
#                 cart_db['cart'] = cart_dict
#     with shelve.open('cart.db','r') as cart_db: 
#         with shelve.open('products.db','r') as product_db:
#             cart_dict = {}
#             product_dict = {}
#             try:
#                 cart_dict = cart_db['cart']
#             except:
#                 print("Error in retrieving Items from cart.db")
#             try:
#                 product_dict = product_db['products']
#             except:
#                 print("Error in retrieving Products from products.db")
#             cart_list_sku = cart_dict.get(user_id)
#             cart_list = []
#             if cart_list_sku is None:
#                 cart_list_sku = []
#             for sku in cart_list_sku:
#                 product = product_dict.get(str(sku))
#                 cart_list.append(product)
#             print(cart_list)
#             print(cart_dict)
#             print(cart_list_sku)

#     return render_template('cart.html', cart_list = cart_list)

# @transactions.route('/remove_cart/<sku>', methods=['POST'])
# def remove_cart(sku):
#     user_id = 1
#     cart_dict = {}
#     cart_db = shelve.open('cart.db', 'w')
#     cart_dict = cart_db['cart']
#     cart_list = cart_dict[user_id]
#     print(cart_list)
#     print(sku)
#     cart_list.pop(int(sku))
#     cart_dict[user_id] = cart_list

#     cart_db['products'] = cart_dict
#     cart_db.close() 

#     return redirect(url_for('main.transactions.cart'))