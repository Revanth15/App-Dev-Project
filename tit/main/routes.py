from flask import render_template, session, Blueprint, request, redirect, url_for
from flask_login import current_user
import shelve
import datetime
import urllib
import json
import hashlib

from tit.admin.inventory.forms import Checkout
from tit.main.transactions.routes import cart, transactions
from tit.main.rewards.routes import rewards
from tit.main.accounts.routes import accounts
from tit.main.support.routes import support
from tit.main.utils import checkoutFunc
from tit.utils import get_db, set_db, event

from tit.classes.Traffic import Session
import tit.classes.payment as Payment
import tit.classes.order as Order



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
    data = [request.path, datetime.datetime.now().strftime('%Y-%m-%d, %H:%M:%S'), request.method, event()]
    sessions_dict = get_db('traffic', 'Sessions')
    viewer = sessions_dict.get(session_id)
    if viewer is None:
        return 'Session ID does not exist'
    viewer.update_views(data)
    sessions_dict[session_id] = viewer
    set_db('traffic', 'Sessions', sessions_dict)
    return f'{session_id} Parsed'
            

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

@main.route('/category/T-Shirts & Tops')
def tops():
    products_dict = {}
    try:
        products_db = shelve.open('tit/database/products.db', 'r')
        products_dict = products_db['products']
        products_db.close()
    except:
        print("Error in retrieving Product from products.db.")

    products_list = []
    category = 'T-Shirts & Tops'
    for key in products_dict:
        product = products_dict.get(key)
        if product.get_category() == category:
            products_list.append(product)
    return render_template('category/product.html', products_list=products_list, category = category)

@main.route('/category/Jeans & Joggers')
def jeans():
    products_dict = {}
    try:
        products_db = shelve.open('tit/database/products.db', 'r')
        products_dict = products_db['products']
        products_db.close()
    except:
        print("Error in retrieving Product from products.db.")

    products_list = []
    category = 'Jeans & Joggers'
    for key in products_dict:
        product = products_dict.get(key)
        if product.get_category() == category:
            products_list.append(product)
    return render_template('category/product.html', products_list=products_list, category = category)

@main.route('/category/Shorts & Skirts')
def shorts():
    products_dict = {}
    try:
        products_db = shelve.open('tit/database/products.db', 'r')
        products_dict = products_db['products']
        products_db.close()
    except:
        print("Error in retrieving Product from products.db.")

    products_list = []
    category = 'Shorts & Skirts'
    for key in products_dict:
        product = products_dict.get(key)
        if product.get_category() == category:
            products_list.append(product)
    return render_template('category/product.html', products_list=products_list, category = category)

@main.route('/category/Dresses')
def dresses():
    products_dict = {}
    try:
        products_db = shelve.open('tit/database/products.db', 'r')
        products_dict = products_db['products']
        products_db.close()
    except:
        print("Error in retrieving Product from products.db.")

    products_list = []
    category = 'Dresses'
    for key in products_dict:
        product = products_dict.get(key)
        if product.get_category() == category:
            products_list.append(product)

    return render_template('category/product.html', products_list=products_list, category = category)

@main.route('/category/Hoodies')
def hoodies():
    products_dict = {}
    try:
        products_db = shelve.open('tit/database/products.db', 'r')
        products_dict = products_db['products']
        products_db.close()
    except:
        print("Error in retrieving Product from products.db.")

    products_list = []
    category = 'Hoodies'
    for key in products_dict:
        product = products_dict.get(key)
        if product.get_category() == category:
            products_list.append(product)
    return render_template('category/product.html', products_list=products_list, category = category)

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


@main.route('/myOrders')
def myOrders():
    user_id = current_user.get_id()
    with shelve.open('tit/database/orders.db', 'w') as orders_db:
        orders_dict = {}
        try:
            orders_dict = orders_db['orders']
        except:
            print("Error in retrieving orders from orders.db")

        orders_list = orders_dict[user_id]
        print(orders_dict)
    return render_template('myorder.html', orders_list=orders_list)

