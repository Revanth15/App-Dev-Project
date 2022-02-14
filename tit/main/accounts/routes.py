import shelve
from flask import flash, redirect, render_template, request, url_for, Blueprint

import tit.classes.Customer as Customer
from tit.classes.admin import Admin
from tit.main.accounts.Forms import CustomerSignUpForm, ChangePasswordForm, getOTPForm

from flask_login import login_required

accounts = Blueprint('accounts', __name__, template_folder='templates', static_url_path='static', url_prefix='/user')


@accounts.route('/getOTP', methods=['GET', 'POST'])
def getOTP():
    get_OTP_form = getOTPForm(request.form)
    if request.method == 'POST':
        customers_dict = {}
        db = shelve.open('tit/database/users.db', 'r')
        try:
            customers_dict = db['Customers']
            for customer in customers_dict.values():
                if customer.get_phone_numbernumber() == get_OTP_form.phone_number.data:
                    print('Customer keyed in the correct number.')
                    redirect(url_for("main.accounts.login"))

        except:
            print("Error in retrieving Customer's Phone Number from users.db")

    return render_template('accounts/getOTP.html', form=get_OTP_form)



# Customer Creates Account / Register
@accounts.route('/signUp', methods=['GET', 'POST'])
def sign_up():
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    user_signup_form = CustomerSignUpForm(request.form)
    if request.method == 'POST':
        users_dict = {}
        db = shelve.open('tit/database/users.db', 'c')
        try:
            count = db['Count']
        except:
            count = 0
            print("Error in retrieving Count from users.db.")


        if 'admin@tit.com' in user_signup_form.email.data:
            try:
                users_dict = db['Admins']
            except:
                print("Error in retrieving Admins from users.db.")
            admin = Admin(user_signup_form.name.data, 
                            user_signup_form.email.data,                         
                            user_signup_form.gender.data, 
                            user_signup_form.phone_number.data, 
                            user_signup_form.password.data, 
                            user_signup_form.confirm_password.data,
                            'Admin')
            if len(users_dict) > 0:
                admin.set_admin_id(list(users_dict)[-1]+1)

            count += 1
            admin.set_user_id(count)
            users_dict[admin.get_admin_id()] = admin
            db['Admins'] = users_dict
            db['Count'] = count

        else:
            try:
                users_dict = db['Customers']
            except:
                print("Error in retrieving Customers from users.db.")
            customer = Customer.Customer(user_signup_form.name.data, 
                            user_signup_form.email.data,                         
                            user_signup_form.gender.data, 
                            user_signup_form.phone_number.data, 
                            user_signup_form.password.data, 
                            user_signup_form.confirm_password.data)

            if len(users_dict) > 0:
                customer.set_customer_id(list(users_dict)[-1]+1)

            count += 1
            customer.set_user_id(count)
            users_dict[customer.get_customer_id()] = customer
            db['Customers'] = users_dict
            db['Count'] = count

            # Test codes
            # users_dict = db['Customers']
            # customer = users_dict[customer.get_customer_id()]
            # print(customer.get_name(), "was stored in users.db successfully with customer_id ==", customer.get_customer_id())
            # print(db['Customers'])       
        db.close()

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
        
    return render_template('signUp.html', form=user_signup_form)




# Customer Retrieve Own Profile
@accounts.route('/retrieveProfile')
@login_required
def retrieveProfile():

    return render_template('accounts/retrieveProfile.html')



# Customer Updates profile
@accounts.route('/updateProfile/<int:id>/', methods=['GET', 'POST'])
@login_required
def update_profile(id):
    update_customer_form = CustomerSignUpForm(request.form)
    if request.method == 'POST':
        users_dict = {}
        db = shelve.open('tit/database/users.db', 'w')
        users_dict = db['Customers']

        customer = users_dict.get(id)
        customer.set_name(update_customer_form.name.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_phone_number(update_customer_form.phone_number.data)

        db['Customers'] = users_dict
        db.close()

        return redirect(url_for('main.accounts.retrieveProfile'))
    else:
        users_dict = {}
        db = shelve.open('tit/database/users.db', 'r')

        try:
           users_dict = db['Customers']
        except:
           print("Error in retrieving customer profile from users.db.")

        customer = users_dict.get(id)
        update_customer_form.name.data = customer.get_name()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.phone_number.data = customer.get_phone_number()

        db.close()

# PROMPT: CUSTOMER PROFILE HAS BEEN UPDATED
        return render_template('accounts/updateProfile.html', form=update_customer_form)

# Customer Enter correct Password, then direct to change password page
@accounts.route('/retrievePassword', methods=['GET','POST'])
@login_required
def retrieve_password():
    change_password_form = ChangePasswordForm(request.form)  
    if request.method == 'POST':
        if change_password_form.password.data == 'adminTime':
            flash("Type in your new password.")
        else:
            users_dict = {}
            db = shelve.open('tit/database/users.db', 'r')
        
            try:
                users_dict = db['Customers']
                for customer in users_dict.values():
                    if customer.get_password() == change_password_form.password.data:
                        redirect()
                        print('Customer keyed in the correct password.')
                        flash('You are able to change password.')
                        redirect(url_for("main.accounts.update_password"))
                        # redirect(url_for("updatePassword/<int:id>/"))

            except:
                print("Error in retrieving Customers from users.db")

        # return redirect(url_for('main.accounts.update_password/<int:id>/'))
    return render_template('accounts/retrievePassword.html', form=change_password_form)


# Update/Change Password
@accounts.route('/updatePassword/<int:id>/', methods=['GET', 'POST'])
@login_required
def update_password(id):
    update_password_form = CustomerSignUpForm(request.form)
    if request.method == 'POST':
        users_dict = {}
        db = shelve.open('tit/database/users.db', 'w')
        users_dict = db['Customers']

        customer = users_dict.get(id)
        customer.set_password(update_password_form.password.data)
        customer.set_confirm_password(update_password_form.confirm_password.data)
        db['Customers'] = users_dict
        db.close()

        return redirect(url_for('main.accounts.retrievePassword'))
    else:
        users_dict = {}
        db = shelve.open('tit/database/users.db', 'r')

        try:
           users_dict = db['Customers']
        except:
           print("Error in retrieving customer profile from users.db.")

        users_dict = db['Customers']
        db.close()

        customer = users_dict.get(id)
        update_password_form.password.data = customer.get_password()
        update_password_form.confirm_password.data = customer.get_confirm_password()


        # PROMPT: CUSTOMER PROFILE HAS BEEN UPDATED
        return render_template('accounts/updateAdminPW.html', form=update_password_form)




# Customer Deletes Account
@accounts.route('/deleteAccount/<int:id>', methods=['POST'])
@login_required
def delete_account(id):
    users_dict = {}
    db = shelve.open('tit/database/users.db', 'w')

    try: 
        users_dict = db['Customers']
    except:
        print("Error in retrieving Customers from users.db.")

    # users_dict = db['Customers']  
    # PROMPT: ARE YOU SURE YOU WANT TO DELETE ACCOUNT?
    # back to HOMEPAGE
    users_dict.pop(id)
    db['Customers'] = users_dict
    db.close()

    return redirect(url_for('main.accounts.sign_up'))

# Customer Forgot Password (Do last)