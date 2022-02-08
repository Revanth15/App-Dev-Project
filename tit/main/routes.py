from flask import render_template, session, Blueprint, request, redirect, url_for
import shelve
import datetime
import urllib
import json
import hashlib

from tit.classes.Traffic import Session
from tit.utils import get_db, set_db, parseVisitor

from tit.main.transactions.routes import transactions
from tit.main.rewards.routes import rewards
from tit.main.accounts.routes import accounts
from tit.main.support.routes import support
import tit.classes.payment as Payment



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
            

@main.route('/', methods=['GET', 'POST'])
def home():
    data = ['home', datetime.datetime.now().strftime('%Y-%m-%d, %H:%M:%S'), request.method]
    print(session['user'])
    print(parseVisitor(data, session['user']))
    products_dict = {}
    session['cart'] = []
    try:
        products_db = shelve.open('tit/database/products.db', 'r')
        products_dict = products_db['products']
        products_db.close()
    except:
        print("Error in retrieving Product from products.db.")

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    return render_template('homepage.html',products_list=products_list)

@main.route('/payment', methods=['GET', 'POST'])
def payment():
    payment_form = PaymentForm()
    if request.method == 'POST' and payment_form.validate_on_submit():
        with shelve.open('tit/database/payment.db', 'c') as payment_db:
            payment_dict = {}

            try:
                payment_dict = payment_db['payment']
            except:
                print("Error in retrieving Info from payment.db")

            payment = Payment.Payment(
                card_number = payment_form.card_number.data,
                card_holder = payment_form.card_holder.data,
                exp_mm = payment_form.exp_mm.data,
                exp_yy = payment_form.exp_yy.data,
                cvv = payment_form.cvv.data)

            current_time = datetime.datetime.now()
            year = str(current_time.year)
            month = str(current_time.month)

            exp_mm = payment.get_exp_mm()
            exp_yy = payment.get_exp_yy()
            print(payment.get_card_number())
            print( exp_mm + exp_yy)
            print( month + year)
            
            if year < exp_yy :
                if month <= exp_mm:
                    card_number = payment.get_card_number()
                    temp = str(card_number)

                    sum_1 = 0
                    sum_2 = 0

                    index = len(temp) - 1

                    while index >= 0:
                        sum_1 += int(temp[index])
                        index -= 2

                    index = len(temp) - 2
                    while index >= 0:
                        number = int(temp[index]) * 2
                        if number >= 10:
                            number = str(number)
                            sum_2 += int(number[0]) + int(number[1])
                        else:
                            sum_2 += number
                        index -= 2

                    sum_of_total = str(sum_2 + sum_1)
                    validation = int(sum_of_total[len(sum_of_total) - 1])

                    if validation == 0:
                        print("card is valid")
                    else:
                        print("card is invalid")
            elif year == exp_yy :
                if month < exp_mm:
                    card_number = payment.get_card_number()
                    temp = str(card_number)

                    sum_1 = 0
                    sum_2 = 0

                    index = len(temp) - 1

                    while index >= 0:
                        sum_1 += int(temp[index])
                        index -= 2

                    index = len(temp) - 2
                    while index >= 0:
                        number = int(temp[index]) * 2
                        if number >= 10:
                            number = str(number)
                            sum_2 += int(number[0]) + int(number[1])
                        else:
                            sum_2 += number
                        index -= 2

                    sum_of_total = str(sum_2 + sum_1)
                    validation = int(sum_of_total[len(sum_of_total) - 1])

                    if validation == 0:
                        print("card is valid")
                    else:
                        print("card is invalid")
            else:
                print("card is invalidddddd")

            payment_dict[payment.get_card_number()] = payment
            payment_db['payment'] = payment_dict
            return redirect(url_for('main.home'))
    return render_template('payment.html', form=payment_form)
