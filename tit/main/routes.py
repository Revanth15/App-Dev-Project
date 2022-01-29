from flask import render_template, session, Blueprint, request, redirect, url_for
from tit.admin.inventory.forms import PaymentForm
import shelve
import datetime

from tit.main.transactions.routes import transactions
import tit.classes.payment as Payment

main = Blueprint('main', __name__)
main.register_blueprint(transactions)

@main.route('/', methods=['GET', 'POST'])
def home():
    products_dict = {}
    session['cart'] = []
    try:
        products_db = shelve.open('products.db', 'r')
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
        with shelve.open('payment.db', 'c') as payment_db:
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
