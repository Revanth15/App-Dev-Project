from io import SEEK_CUR
from flask import render_template, request, redirect, url_for, Blueprint,session
import shelve
from tit import app 
from flask_login import current_user
from tit.utils import get_db, set_db

transactions = Blueprint('transactions', __name__, template_folder='templates', static_url_path='static', url_prefix='/transactions')

@transactions.route('/cart', methods=['GET','POST'])
def cart(): 
    user_id = current_user.get_customer_id()
    if request.method == 'POST':     
        cart_dict = get_db('cart', 'cart')
        sku = str(request.form['sku'])
        if cart_dict.get(user_id) is None:
            cart_dict[user_id] = [{},0,0]
        
        if sku in cart_dict[user_id][0]:
            cart_dict[user_id][0][sku] += 1
        else:
            cart_dict[user_id][0].update({sku: 1})

        set_db('cart', 'cart', cart_dict)
    cart_dict = get_db('cart', 'cart')
    product_dict = get_db('products', 'products')
    cart = cart_dict.get(user_id)
    if cart is None:
        user_cart = {}
    else:
        user_cart = cart[0]
    cart_list = []
    for sku in user_cart:
        if str(sku) in product_dict:
            product = product_dict.get(str(sku))
            cart_list.append([product,user_cart[sku]])
            print(cart_list)

    user_dict = get_db('users', 'Customers')
    user = user_dict[current_user.get_customer_id()]
    if len(cart_list) > 0:
        user.set_cartStatus('Items in cart')
        user_dict[user.get_customer_id()] = user
    else:
        current_user.set_cartStatus('Empty')
        user_dict[user.get_customer_id()] = user
    set_db('users', 'Customers', user_dict)

    return render_template('inventory/cart.html', cart_list = cart_list)


@transactions.route('/remove_item/<sku>', methods=['POST'])
def remove_item(sku):
    user_id = current_user.get_customer_id()
    cart_dict = get_db('cart', 'cart')
    cart_dict[user_id][0].pop(sku)
    
    set_db('cart', 'cart', cart_dict)

    return redirect(url_for('main.transactions.cart'))

@transactions.route('/delete_cart', methods=['POST'])
def delete_cart():
    user_id = current_user.get_customer_id()
    cart_dict = get_db('cart', 'cart')
    cart_dict.pop(int(user_id))

    set_db('cart', 'cart', cart_dict)

    return redirect(url_for('main.transactions.cart'))

@transactions.route('/update_cart' ,methods=['GET'])
def update_cart():
    user_id = current_user.get_customer_id()
    cart_dict = get_db('cart', 'cart')
    sku = str(request.args.get('sku'))
    quantity = int(request.args.get('quantity'))
    # subtotal = int(request.args.get('subtotal'))
    # print(subtotal)
    if int(quantity) <= 0:
        quantity = 1
    cart_dict[user_id][0].update({sku: quantity})
    set_db('cart', 'cart', cart_dict)
    return '1'


@transactions.route('/update_total' ,methods=['GET', 'POST'])
def update_total():
    user_id = current_user.get_customer_id()
    cart_dict = get_db('cart', 'cart')
    subtotal = int(request.args.get('subtotal'))
    cart_dict[user_id][1] = subtotal
    set_db('cart', 'cart', cart_dict)
    return redirect(url_for('main.checkout'))


@transactions.route('/discount' ,methods=['GET','POST'])
def discount():
    user_id = current_user.get_customer_id()
    discount_code_applied = request.args.get('discount_code')
    cart_dict = get_db('cart', 'cart')
    vouchers_dict = get_db('vouchers', 'Vouchers')
    customers_dict = get_db('users', 'Customers')
    print(cart_dict)
    print(user_id)
    try:
        cart_dict[user_id][2] = discount_code_applied
    except KeyError:
        cart_dict[user_id][2] = None
    print(customers_dict)
    customer = customers_dict.get(user_id)
    spools = customer.get_spools()
    print(spools)
    print(discount_code_applied)
    for key in vouchers_dict:
        voucher = vouchers_dict.get(key)
        print(voucher.get_discount_code())
        if discount_code_applied == voucher.get_discount_code():
            if voucher.get_quantity() > 0:
                spools_needed = int(voucher.get_spools())
                if spools >= spools_needed:
                    discount = voucher.get_discount_amount()
                    print(discount)
                    set_db('cart', 'cart', cart_dict)   
                    return {'discountcode' : discount, 'flash': "Discount Code applied successfully!"}
                else:
                    return  {'discountcode' : 0, 'flash' : "Insufficient spools!"}
            else:
                return  {'discountcode' : 0, 'flash' : "Oh noo,This voucher has been used up!"}
                
    return {'discountcode' : 0, 'flash' : "There is no such voucher code!"}


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