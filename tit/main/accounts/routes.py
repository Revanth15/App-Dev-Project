import shelve
from flask import flash, redirect, render_template, request, url_for, Blueprint

import tit.classes.Customer as Customer
from tit.main.accounts.Forms import CustomerSignUpForm, LoginForm, ChangePasswordForm

from flask_login import login_required, login_user, logout_user

accounts = Blueprint('accounts', __name__, template_folder='templates', static_url_path='static', url_prefix='/user')


# Customer Creates Account / Register
@accounts.route('/signUp', methods=['GET', 'POST'])
def sign_up():
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    customer_signup_form = CustomerSignUpForm(request.form)
    if request.method == 'POST':
        customers_dict = {}
        db = shelve.open('tit/database/customers.db', 'c')

        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving Customers from customers.db.")

        customer = Customer.Customer(customer_signup_form.name.data, 
                        customer_signup_form.email.data,                         
                        customer_signup_form.gender.data, 
                        customer_signup_form.phone_number.data, 
                        customer_signup_form.password.data, 
                        customer_signup_form.confirm_password.data)
        
        if len(customers_dict) > 0:
            customer.set_customer_id(list(customers_dict)[-1]+1)

        customers_dict[customer.get_customer_id()] = customer
        db['Customers'] = customers_dict

        # Test codes
        customers_dict = db['Customers']
        customer = customers_dict[customer.get_customer_id()]
        print(customer.get_name(), "was stored in customers.db successfully with customer_id ==", customer.get_customer_id())
        print(db['Customers'])
        db.close()

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('main.accounts.login'))
        
    return render_template('signUp.html', form=customer_signup_form)



# Customer Login
@accounts.route('/login', methods=['GET','POST'])
def login():
    login_form = LoginForm(request.form)  
    if request.method == 'POST':
        customers_dict = {}
        db = shelve.open('tit/database/customers.db', 'r')
        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving customer profile from customers.db.")
        db.close()
        for customer in customers_dict.values():
            if login_form.email.data == 'admin@tit.com':
                if customer.get_password() == login_form.password.data:
                    print("Admin login successful")
                    flash('You have been logged in', 'success')
                    return(redirect(url_for("admin_home")))
        
            else:
                if customer.get_email() == login_form.email.data:
                    if customer.get_password() == login_form.password.data:
                        login_user(customer, remember=login_form.remember.data)
                        print('Customer login successful')
                        flash('Login Successful')

                        # add a next page route
                        next_page = request.args.get('next')
                        print(next_page)
                        return redirect(next_page) if next_page else redirect(url_for("main.home"))

        flash('Incorrect email or password.')
            
    return render_template('login.html', form=login_form)


# Customer Logout 
@accounts.route("/logout")
@login_required
def logout():
    logout_user
    return redirect(url_for('main.accounts.login'))


# Customer Retrieve Own Profile
@accounts.route('/retrieveProfile/<int:id>/')
@login_required
def retrieveProfile():
    customers_dict = {}

    db = shelve.open('tit/database/customers.db', 'r')
    try:
        customers_dict = db['Customers']
    except:
        print("Error in retrieving Customers from storage.db.")

    db.close()
    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)

    return render_template('accounts/retrieveProfile.html', customers_list=customers_list)



# Customer Updates profile
@accounts.route('/updateProfile/<int:id>/', methods=['GET', 'POST'])
def update_profile(id):
    update_customer_form = CustomerSignUpForm(request.form)
    if request.method == 'POST':
        customers_dict = {}
        db = shelve.open('tit/database/customers.db', 'w')
        customers_dict = db['Customers']

        customer = customers_dict.get(id)
        customer.set_name(update_customer_form.name.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_phone_number(update_customer_form.phone_number.data)

        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('main.accounts.retrieveProfile/<int:id>/'))
    else:
        customers_dict = {}
        db = shelve.open('tit/database/customers.db', 'r')

        try:
           customers_dict = db['Customers']
        except:
           print("Error in retrieving customer profile from customers.db.")

        customer = customers_dict.get(id)
        update_customer_form.name.data = customer.get_name()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.phone_number.data = customer.get_phone_number()

        db.close()

# PROMPT: CUSTOMER PROFILE HAS BEEN UPDATED
        return render_template('accounts/updateProfile.html', form=update_customer_form)

# Customer Enter correct Password, then direct to change password page
@accounts.route('/currentAdminPW', methods=['GET','POST'])
def currentAdminPW():
    change_password_form = ChangePasswordForm(request.form)  
    if request.method == 'POST':
        if change_password_form.password.data == 'adminTime':
            flash("Type in yur new password.")
        else:
            customers_dict = {}
            db = shelve.open('tit/database/customers.db', 'r')
            try:
                customers_dict = db['Customers']
            except:
                print("Error in retrieving Customers from customers.db.")   

            try:
                for customer in customers_dict.values():
                    if customer.get_password() == change_password_form.password.data:
                        redirect()
                        print('Customer keyed in the correct password.')
                        flash('You are able to change password.')
                        redirect(url_for("updatePassword/<int:id>/"))

            except:
                print("Error in retrieving Customers from customers.db")

            else:
                flash('Login Unsuccessful. Please check your password')
                return render_template('currentAdminPW.html', form=change_password_form)
                
            # return redirect(url_for('updatePassword/<int:id>/'))
            return redirect(url_for('main.accounts.updateAdminPW/<int:id>/'))
    return render_template('accounts/currentAdminPW.html', form=change_password_form)


# Update/Change Password
@accounts.route('/updateAdminPW/<int:id>/', methods=['GET', 'POST'])
def update_password(id):
    update_password_form = CustomerSignUpForm(request.form)
    if request.method == 'POST':
        customers_dict = {}
        db = shelve.open('tit/database/customers.db', 'w')
        customers_dict = db['Customers']

        customer = customers_dict.get(id)
        customer.set_password(update_password_form.password.data)
        customer.set_confirm_password(update_password_form.confirm_password.data)
        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('main.accounts.retrievePassword'))
    else:
        customers_dict = {}
        db = shelve.open('tit/database/customers.db', 'r')

        try:
           customers_dict = db['Customers']
        except:
           print("Error in retrieving customer profile from customers.db.")

        customers_dict = db['Customers']
        db.close()

        customer = customers_dict.get(id)
        update_password_form.password.data = customer.get_password()
        update_password_form.confirm_password.data = customer.get_confirm_password()


        # PROMPT: CUSTOMER PROFILE HAS BEEN UPDATED
        return render_template('accounts/updateAdminPW.html', form=update_password_form)




# Customer Deletes Account
@accounts.route('/deleteAccount/<int:id>', methods=['POST'])
def delete_account(id):
    customers_dict = {}
    db = shelve.open('tit/database/customers.db', 'w')

    try: 
        customers_dict = db['Customers']
    except:
        print("Error in retrieving Customers from customers.db.")

    # customers_dict = db['Customers']  
    # PROMPT: ARE YOU SURE YOU WANT TO DELETE ACCOUNT?
    # back to HOMEPAGE
    customers_dict.pop(id)
    db['Customers'] = customers_dict
    db.close()

    return redirect(url_for('main.accounts.signUp'))

# Customer Forgot Password (Do last)