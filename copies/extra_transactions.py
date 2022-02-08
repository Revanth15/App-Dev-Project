from flask import render_template, request, redirect, url_for, session
from tit.admin.inventory.forms import CreateProductForm, RestockForm, ImportForm, PaymentForm, Delivery
from flask_recaptcha import ReCaptcha
import datetime
import os
import shelve
import tit.classes.product as Product
import tit.classes.delivery as Delivery
import tit.classes.import_file as import_file
import tit.classes.payment as Payment
import tit.classes.cart as Cart
from tit.utils import display
import uuid
from tit import app 




# @app.route('/delivery/<cust_id>/', method=['GET', 'POST'])
# def delivery(cust_id):
#     delivery_form = Delivery()
#     if request.method == 'POST' and delivery_form.validate():
#         with shelve.open('delivery.db', 'w') as delivery_db:
#             delivery_dict = {}
#             delivery_dict = delivery_db['delivery']

#             delivery = delivery_dict.get(cust_id)
#             product.set_first_name(delivery_form.first_name.data)
#             product.set_last_name(delivery_form.last_name.data)
#             product.set_address(delivery_form.address.data)
#             product.set_unit_number(delivery_form.unit_number.data)
#             product.set_postal_code(delivery_form.postal_code.data)
#             product.set_email(delivery_form.email.data)
#             product.set_phone_number(delivery_form.phone_number.data)

#             delivery_db['delivery'] = delivery_dict

#             return redirect(url_for('payment'))
#     else:
#         with shelve.open('delivery.db', 'r') as delivery_db:
#             delivery_dict = {}
#             delivery_db = shelve.open('delivery.db', 'r')
#             delivery_dict = delivery_db['delivery']

#             delivery = delivery_dict.get(cust_id)
#             delivery_form.first_name.data = delivery.get_first_name()
#             delivery_form.last_name.data = delivery.get_last_name()
#             delivery_form.address.data = delivery.get_address()
#             delivery_form.unit_number.data = delivery.get_unit_number()
#             delivery_form.postal_code.data = delivery.get_postal_code()
#             delivery_form.email.data = delivery.get_email()
#             delivery_form.phone_number.data = delivery.get_phone_number()
#         return render_template('delivery.html', form=delivery_form)


# @app.route('/cart', methods=['GET','POST'])
# def cart(): 
#     user_id = 1
#     if request.method == 'POST':
#         with shelve.open('cart.db','c') as cart_db:
#             cart_dict = {}
#             try:
#                 cart_dict = cart_db['cart']
#             except:
#                 print("Error in retrieving Items from cart.db")
#             cart_list = cart_dict.get(user_id)
#             if cart_list is None:
#                 cart_list = []
#             sku = int(request.form['sku'])
#             cart_list.append(sku)
#             cart_dict[user_id] = cart_list
#             cart_db['cart'] = cart_dict
#             print(cart_dict)
#     return render_template('cart.html', cart_list = cart_list)




