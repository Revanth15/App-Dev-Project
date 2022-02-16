from flask import flash, render_template, session, Blueprint, request, redirect, url_for
from flask_login import current_user, login_required
import shelve
import datetime
import urllib
import json
import hashlib


from tit.main.transactions.routes import transactions
from tit.main.rewards.routes import rewards
from tit.main.accounts.routes import accounts
from tit.main.support.routes import support
from tit.main.utils import checkoutFunc
from tit.utils import dbkeys, get_db, set_db, event

from tit.classes.Traffic import Session
import tit.classes.payment as Payment
from tit.admin.inventory.forms import Checkout


main = Blueprint('main', __name__)
main.register_blueprint(transactions)
main.register_blueprint(rewards)
main.register_blueprint(accounts)
main.register_blueprint(support)


@main.before_request
def getSession():
    if 'static' not in request.url:
        time = datetime.datetime.now().replace(microsecond=0)
        userIP = request.remote_addr
        if 'user' not in session:
            lines = (str(time)+userIP).encode('utf-8')
            session['user'] = hashlib.md5(lines).hexdigest()
            sessionID = session['user']
        else:
            sessionID = session['user']
        
        sessions_dict = get_db('traffic', 'Sessions')
        if sessionID not in sessions_dict:
            api = "https://www.iplocate.io/api/lookup/" + userIP
            userCity = None
            userContinent = None
            userCountry = None
            try:
                resp = urllib.request.urlopen(api)
                result = resp.read()
                result = json.loads(result.decode("utf-8"))                                                                                                     
                userCountry = result["country"]
                userContinent = result["continent"]
                userCity = result["city"]
            except:
                print("Could not find: ", userIP)
            viewer = Session(userIP, sessionID, userCountry, userContinent, userCity)
            sessions_dict[viewer.get_session()] =  viewer
            set_db('traffic', 'Sessions', sessions_dict)
        parseVisitorData(sessionID)

def parseVisitorData(session_id):
    data = [request.path, datetime.datetime.now(), event()]
    sessions_dict = get_db('traffic', 'Sessions')
    viewer = sessions_dict.get(session_id)
    if viewer is None:
        return 'Session ID does not exist'
    viewer.update_views(data)
    sessions_dict[session_id] = viewer
    set_db('traffic', 'Sessions', sessions_dict)
    return f'{session_id} Parsed'
            

@main.route('/')
def home():
    products_dict = get_db('products', 'products')

    products_list = []
    i = 1
    for key in products_dict:
        product = products_dict.get(key)
        if i <= 8:
            if product.get_quantity() >= 10:
                products_list.append(product)
                i += 1
        else:
            break

    return render_template('homepage.html',products_list=products_list)

@main.route('/category/T-Shirts & Tops')
def tops():
    products_dict = get_db('products', 'products')

    products_list = []
    category = 'T-Shirts & Tops'
    for key in products_dict:
        product = products_dict.get(key)
        if product.get_category() == category:
            products_list.append(product)
    return render_template('category/product.html', products_list=products_list, category = category)

@main.route('/category/Jeans & Joggers')
def jeans():
    products_dict = get_db('products', 'products')

    products_list = []
    category = 'Jeans & Joggers'
    for key in products_dict:
        product = products_dict.get(key)
        if product.get_category() == category:
            products_list.append(product)
    return render_template('category/product.html', products_list=products_list, category = category)

@main.route('/category/Shorts & Skirts')
def shorts():
    products_dict = get_db('products', 'products')

    products_list = []
    category = 'Shorts & Skirts'
    for key in products_dict:
        product = products_dict.get(key)
        if product.get_category() == category:
            products_list.append(product)
    return render_template('category/product.html', products_list=products_list, category = category)

@main.route('/category/Dresses')
def dresses():
    products_dict = get_db('products', 'products')

    products_list = []
    category = 'Dresses'
    for key in products_dict:
        product = products_dict.get(key)
        if product.get_category() == category:
            products_list.append(product)

    return render_template('category/product.html', products_list=products_list, category = category)

@main.route('/category/Hoodies')
def hoodies():
    products_dict = get_db('products', 'products')

    products_list = []
    category = 'Hoodies'
    for key in products_dict:
        product = products_dict.get(key)
        if product.get_category() == category:
            products_list.append(product)
    return render_template('category/product.html', products_list=products_list, category = category)

@main.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    user_id = current_user.get_customer_id()
    checkout_form = Checkout()
    if request.method == 'POST' and checkout_form.validate_on_submit():
        payment_dict = get_db('payment','payment')

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
        print(year, month, exp_mm, exp_yy)

        if year < exp_yy :
            checkoutFunc()

        elif year == exp_yy :
            if month < exp_mm:
                checkoutFunc()
            else:
                print("card is expired")
        else:
            print("card is expired")

        payment_dict[payment.get_card_number()] = payment
        set_db('payment','payment', payment_dict)
        current_user.set_cartStatus('Purchased')
        return redirect(url_for('main.home'))
    else:
        customers_dict = get_db('users', 'Customers')

        customer = customers_dict.get(user_id)
        checkout_form.name.data = customer.get_name()
        checkout_form.email.data = customer.get_email()
        checkout_form.phone_number.data = customer.get_phone_number()
        return render_template('checkout.html', form=checkout_form)

@main.route('/cancelOrder')
@login_required
def cancel():
    user_dict = get_db('users', 'Customers')
    user = user_dict[current_user.get_customer_id()]
    if current_user.get_role() == 'Customer':
        user.set_cartStatus('Cancelled')
        user_dict[user.get_customer_id()] = user
        set_db('users', 'Customers', user_dict)
    return redirect(url_for('main.transactions.cart'))

@main.route('/myOrders')
@login_required
def myOrders():
    user_id = current_user.get_customer_id()
    orders_dict = get_db('orders', 'orders')
        
    order_list = []
    if orders_dict.get(user_id) is not None:
        for key in orders_dict[user_id]:
            order = orders_dict[user_id].get(key)
            order_id = key
            status = order.get_status()
            order_list.append([order,order_id,status])
    else:
        order_list = []
    print(order_list)
    return render_template('myorder.html', orders_list=order_list)

@main.route('/order/<id>/', methods=['GET', 'POST'])
@login_required
def order(id):
    user_id = current_user.get_customer_id()
    orders_dict = get_db('orders', 'orders')
    products_dict = get_db('products', 'products')
    products_list = []
    print(orders_dict)
    order = orders_dict[user_id].get(id)
    for sku in order.get_order():
        product = products_dict.get(sku)
        dict = order.get_order()
        qty = dict[sku]
        products_list.append([product,qty,order])

    return render_template('order.html',products_list=products_list)

# edit users
# delete
# forget password
# validation