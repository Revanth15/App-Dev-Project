import shelve
from flask_login import current_user

import tit.classes.order as Order
from tit.utils import get_db, set_db

def checkoutFunc():
    user_id = current_user.get_customer_id()
    cart_dict = get_db('cart', 'cart')
    customers_dict = get_db('users', 'Customers')
    orders_dict = get_db('orders', 'orders')
    products_dict = get_db('products', 'products')
                    
    if cart_dict.get(user_id) is None:
        cart_dict[user_id] = [{},0,0]

    cart = cart_dict[user_id]
    status = 'Processing'
    order = Order.Order(cart[1],cart[0],status)
    order_id = order.get_order_id()
    if orders_dict.get(user_id) is not None:
        cust_order = orders_dict.get(user_id) 
    else:
        cust_order = {}
    cust_order.update({order_id : order})
    orders_dict[user_id] = cust_order

    vouchers_dict = get_db('vouchers', 'Vouchers')
    
    discount_code_applied = cart_dict[user_id][2]
    for key in vouchers_dict:
        voucher = vouchers_dict.get(key)
        if discount_code_applied == voucher.get_discount_code():
            qty = voucher.get_quantity() - 1
            voucher.set_quantity(qty)
            vouchers_dict[key] = voucher

    # hand out spools
    order_total = cart_dict[user_id][1]
    spools = current_user.get_spools() + int(order_total)
    customer = customers_dict[user_id]
    customer.set_spools(spools)
    print(order_total)
    print(spools)
    customers_dict[user_id] = customer

    # minus qty
    cart = cart_dict.get(user_id)
    user_cart = cart[0]
    for sku in user_cart:
        product = products_dict.get(sku)
        qty = product.get_quantity() - cart_dict[user_id][0][sku]
        product.set_quantity(qty)
        
    cart_dict.pop(int(user_id))
    set_db('cart', 'cart', cart_dict)
    set_db('orders', 'orders', orders_dict)
    set_db('vouchers', 'Vouchers', vouchers_dict)
    set_db('products', 'products', products_dict)
    set_db('users', 'Customers', customers_dict)