from fileinput import filename
from hashlib import md5
import os
import shelve
from click import File
import email_validator
from flask import (Flask, flash, redirect, render_template, request, make_response, url_for, session, abort) 
import email_validator
import tit.classes.User as User, tit.classes.Customer as Customer
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_bcrypt import Bcrypt

# g for global variables

from tit.main.accounts.Forms import LoginForm, CustomerSignUpForm, OldPasswordForm

app = Flask(__name__)
bcrypt = Bcrypt(app)
# we add functionality to db models, it will handle sessions in the background
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.secret_key = os.urandom(24)

@app.route('/')
def home():
    return render_template('base.html')
  
@app.route('/admin_navbar')
def admin_navbar():
    return render_template('admin_navbar.html')

@login_manager.user_loader
def load_user(customer_id):
    customers_dict = {}
    db = shelve.open('customer.db', 'c')
    if 'customers_dict' in db:
        customers_dict = db['Customers']
    else: 
        db['Customers'] = customers_dict
    # given id, return customer object
    customer = customers_dict.get(customer_id)
    db.close()
    if customer:
        return customer


# Customer Creates Account / Register
@app.route('/signUp', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    customer_signup_form = CustomerSignUpForm(request.form)
    if request.method == 'POST':
        customers_dict = {}
        db = shelve.open('customer.db', 'c')

        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving Customers from customer.db.")

        #hash_password = bcrypt.generate_password_hash(customer_signup_form.password.data)
        #hash_confirm_password = bcrypt.generate_password_hash(customer_signup_form.confirm_password.data)
        customer = Customer.Customer(customer_signup_form.name.data, 
                        customer_signup_form.email.data,                         
                        customer_signup_form.gender.data, 
                        customer_signup_form.phone_number.data, 
                        customer_signup_form.password.data, 
                        customer_signup_form.confirm_password.data)
        
        customers_dict[customer.get_customer_id()] = customer
        db['Customers'] = customers_dict
        
        # Test codes
        customers_dict = db['Customers']
        customer = customers_dict[customer.get_customer_id()]
        print(customer.get_name(), "was stored in customer.db successfully with customer_id ==", customer.get_customer_id())

        db.close()

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
        
    return render_template('signUp.html', form=customer_signup_form)
    

# Customer Login
@app.route('/login', methods=['GET','POST'])
def login():
    login_form = LoginForm(request.form)        
    if request.method == 'POST' and login_form.validate():
        if login_form.email.data == 'admin@tit.com' and login_form.password.data == 'adminTime':
            flash('You have been logged in', 'success')

        else:
            customers_dict = {}
            db = shelve.open('customers.db', 'r')

            if 'customers_dict' in db:
                customers_dict = db['Customers']

            try:
                for customer in customers_dict.values():
                    if customer.get_email() == login_form.data:
                        if customer.get_password() == login_form.password.data:
                            login_user(customer, remember=login_form.remember.data)

                            # add a next page route
                            next_page = request.args.get('next')
                            return redirect(next_page) if next_page else redirect(url_for("home"))
            except:
                print("Error in retrieving Customers from customers.db")

            else:
                db['Customers'] = customers_dict
                db.close
                flash('Login Unsuccessful. Please check email and password', '')
        return render_template('signUp.html', form=login_form)
        
    return render_template('signUp.html', form=login_form)



# Customer Logout 
@app.route("/logout")
@login_required
def logout():
    logout_user
    return redirect(url_for('home'))



# Customer Retrieve Own Profile
@app.route('/retrieveProfile/<int:id>/')
@login_required
def retrieveProfile():
    customers_dict = {}
    db = shelve.open('customer.db', 'r')

    try:
        customers_dict = db['Customers']
    except:
        print("Error in retrieving Customers from storage.db.")

    customers_dict = db['Customers']
    db.close()

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)

    return render_template('retrieveProfile.html', customers_list=customers_list)


# Customer Updates profile
@app.route('/updateProfile/<int:id>/', methods=['GET', 'POST'])
def update_profile(id):
    update_customer_form = CustomerSignUpForm(request.form)
    if request.method == 'POST':
        customers_dict = {}
        db = shelve.open('customer.db', 'w')
        customers_dict = db['Customers']

        customer = customers_dict.get(id)
        customer.set_name(update_customer_form.name.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_phone_number(update_customer_form.phone_number.data)

        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('retrieveProfile'))
    else:
        customers_dict = {}
        db = shelve.open('customer.db', 'r')

        try:
           customers_dict = db['Customers']
        except:
           print("Error in retrieving customer profile from customer.db.")

        customers_dict = db['Customers']
        db.close()

        customer = customers_dict.get(id)
        update_customer_form.name.data = customer.get_name()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.phone_number.data = customer.get_phone_number()

# PROMPT: CUSTOMER PROFILE HAS BEEN UPDATED
        return render_template('updateProfile.html', form=update_customer_form)



# Customer type old password, if wrong cannot change/ reset password 
@app.route('/oldPassword/<int:id>/', methods=['GET','POST'])
def old_password():
    old_password_form = CustomerSignUpForm(request.form)        
    if request.method == 'POST' and old_password_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'r')

        if 'customers_dict' in db:
            customers_dict = db['Customers']

        try:
            for customer in customers_dict.values():
                if customer.get_password() == old_password_form.data:
        
                    # add a next page route
                    next_page = request.args.get('next')
                    return redirect(next_page) if next_page else redirect(url_for("update_password"))
        except:
            print("Error in retrieving Customer's old password from customer.db")

        else:
            db['Customers'] = customers_dict
            db.close
            flash('Change Password Unsuccessful. Please check your old password.')

    return render_template('oldPassword.html', form=old_password_form)


# Customer Updates Password
@app.route('/updatePassword/<int:id>/', methods=['GET', 'POST'])
def update_password(id):
    update_password_form = CustomerSignUpForm(request.form)
    if request.method == 'POST':
        customers_dict = {}
        db = shelve.open('customer.db', 'w')
        customers_dict = db['Customers']

        customer = customers_dict.get(id)
        customer.set_password(update_password_form.password.data)
        customer.set_confirm_password(update_password_form.confirm_password.data)
        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('retrievePassword'))
    else:
        customers_dict = {}
        db = shelve.open('customer.db', 'r')

        try:
           customers_dict = db['Customers']
        except:
           print("Error in retrieving customer profile from customer.db.")

        customers_dict = db['Customers']
        db.close()

        customer = customers_dict.get(id)
        update_password_form.password.data = customer.get_password()
        update_password_form.confirm_password.data = customer.get_confirm_password()


# PROMPT: CUSTOMER PROFILE HAS BEEN UPDATED
        return render_template('updatePassword.html', form=update_password_form)



# Customer Deletes Account
@app.route('/deleteAccount/<int:id>', methods=['POST'])
def delete_customer(id):
    customers_dict = {}
    db = shelve.open('customer.db', 'w')

    try: 
        customers_dict = db['Customers']
    except:
        print("Error in retrieving Customers from customer.db.")

    # customers_dict = db['Customers']  
    # PROMPT: ARE YOU SURE YOU WANT TO DELETE ACCOUNT?
    # back to HOMEPAGE
    customers_dict.pop(id)
    db['Customers'] = customers_dict
    db.close()

    return redirect(url_for('signUp'))





# Customer Resets Password (DO LAST)


# Admin - Retrieve Customers
@app.route('/retrieveCustomers')
def retrieveCustomers():
    customers_dict = {}
    db = shelve.open('customer.db', 'r')

    try:
        customers_dict = db['Customers']
    except:
        print("Error in retrieving Customers from storage.db.")

    customers_dict = db['Customers']
    db.close()

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)

    return render_template('retrieveCustomers.html', count=len(customers_list), customers_list=customers_list)



# Admin Updates Customer profile
@app.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    update_customer_form = CustomerSignUpForm(request.form)
    if request.method == 'POST':
        customers_dict = {}
        db = shelve.open('customer.db', 'w')
        customers_dict = db['Customers']

        customer = customers_dict.get(id)
        customer.set_name(update_customer_form.name.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_phone_number(update_customer_form.phone_number.data)
        customer.set_password(update_customer_form.password.data)

        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('retrieveCustomers'))
    else:
        customers_dict = {}
        db = shelve.open('customer.db', 'r')

        try:
           customers_dict = db['Customers']
        except:
           print("Error in retrieving customer from customer.db.")

        customers_dict = db['Customers']
        db.close()

        customer = customers_dict.get(id)
        update_customer_form.name.data = customer.get_name()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.phone_number.data = customer.get_phone_number()
        update_customer_form.password.data = customer.get_password()

        return render_template('updateCustomer.html', form=update_customer_form)


# Admin deletes customer
@app.route('/deleteCustomer/<int:id>', methods=['POST'])
def delete_customer(id):
    customers_dict = {}
    db = shelve.open('customer.db', 'w')

    try: 
        customers_dict = db['Customers']
   
    except:
        print("Error in retrieving Customers from customer.db.")

    # customers_dict = db['Customers']  

    customers_dict.pop(id)

    db['Customers'] = customers_dict
    db.close()

    return redirect(url_for('retrieveCustomers'))


@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


# # SET COOKIES
# @app.route('/setcookie')
# def setcookie():
#     resp = make_response(render_template("home.html"))
#     resp.set_cookie('email', 'WONG ZE')
#     return resp


# # GET COOKIES
# @app.route('getcookie')
# def getcookie():
#     email = request.cookies.get('email', "Default Name")
#     return email



    #   customers_list.append(customer_email)
     #  customers_list.append(customer_password)

if __name__ == '__main__':
    app.run(debug=True)


