from flask import render_template, session, Blueprint, request, redirect, url_for
from tit.admin.inventory.forms import Checkout
import shelve
import datetime
from flask_login import current_user

from tit.main.transactions.routes import cart, transactions
from tit.main.rewards.routes import rewards
from tit.main.accounts.routes import accounts
from tit.main.support.routes import support
import tit.classes.payment as Payment
import tit.classes.order as Order
from tit.main.utils import checkoutFunc

main = Blueprint('main', __name__)
main.register_blueprint(transactions)
main.register_blueprint(rewards)
main.register_blueprint(accounts)
main.register_blueprint(support)

@main.route('/', methods=['GET', 'POST'])
def home():
    products_dict = {}
    try:
        products_db = shelve.open('tit/database/products.db', 'r')
        products_dict = products_db['products']
        products_db.close()
    except:
        print("Error in retrieving Product from products.db.")

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        if product.get_quantity() >= 5:
            products_list.append(product)

    return render_template('homepage.html',products_list=products_list)

# @main.route('/category/<str:category>')
# def category():
#     pass
#     return '1'

# @main.route('/payment', methods=['GET', 'POST'])
# def payment():
#     payment_form = PaymentForm()
#     if request.method == 'POST' and payment_form.validate_on_submit():
#         with shelve.open('tit/database/payment.db', 'c') as payment_db:
#             payment_dict = {}

#             try:
#                 payment_dict = payment_db['payment']
#             except:
#                 print("Error in retrieving Info from payment.db")

#             payment = Payment.Payment(
#                 card_number = payment_form.card_number.data,
#                 card_holder = payment_form.card_holder.data,
#                 exp_mm = payment_form.exp_mm.data,
#                 exp_yy = payment_form.exp_yy.data,
#                 cvv = payment_form.cvv.data)

#             current_time = datetime.datetime.now()
#             year = str(current_time.year)
#             month = str(current_time.month)

#             exp_mm = payment.get_exp_mm()
#             exp_yy = payment.get_exp_yy()
            
#             if year < exp_yy :
#                 if month <= exp_mm:
#                     pass
#             elif year == exp_yy :
#                 if month < exp_mm:
#                     pass
#             else:
#                 print("card is invalidddddd")

#             payment_dict[payment.get_card_number()] = payment
#             payment_db['payment'] = payment_dict
#             return redirect(url_for('main.home'))
#     return render_template('shipping.html', form=payment_form)

@main.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cust_id = current_user.get_id()
    checkout_form = Checkout()
    if request.method == 'POST' and checkout_form.validate_on_submit():
        with shelve.open('tit/database/payment.db', 'c') as payment_db:
            payment_dict = {}

            try:
                payment_dict = payment_db['payment']
            except:
                print("Error in retrieving Info from payment.db")

            payment = Payment.Payment(
                card_number = checkout_form.card_number.data,
                card_holder = checkout_form.card_holder.data,
                exp_mm = checkout_form.exp_mm.data,
                exp_yy = checkout_form.exp_yy.data,
                cvv = checkout_form.cvv.data)

            current_time = datetime.datetime.now()
            year = str(current_time.year)
            month = str(current_time.month)

            exp_mm = payment.get_exp_mm()
            exp_yy = payment.get_exp_yy()

            if year < exp_yy :
                if month <= exp_mm:
                    checkoutFunc()

            elif year == exp_yy :
                if month > exp_mm:
                    checkoutFunc()
            else:
                print("card is invalidddddd")

            payment_dict[payment.get_card_number()] = payment
            payment_db['payment'] = payment_dict
            return redirect(url_for('main.home'))
    else:
        with shelve.open('tit/database/customers.db', 'r') as customer_db:
            customer_dict = {}
            try: 
                customer_dict = customer_db['Customers']
            except:
                print("Error in retrieving Customers from customers.db.")

            customer = customer_dict.get(cust_id)
            checkout_form.name.data = customer.get_name()
            checkout_form.email.data = customer.get_email()
            checkout_form.phone_number.data = customer.get_phone_number()
        return render_template('checkout.html', form=checkout_form)


@main.route('/applycode', methods=['POST'])
def apply():
    user_id = current_user.get_id()
    with shelve.open('tit/database/cart.db', 'c') as cart_db:
        cart_dict = {}
        try:
            cart_dict = cart_db['cart']
        except:
            print("Error in retrieving Items from cart.db")
        print(cart_dict)
        print(user_id)
        try:
            cart_dict[user_id][2] = request.form['discountcode']
        except KeyError:
            cart_dict[user_id][2] = None
        cart_db['cart'] = cart_dict
    return redirect(url_for('main.checkout'))
