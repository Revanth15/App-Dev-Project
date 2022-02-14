import shelve
from tit.main.accounts.Forms import ChangePasswordForm, CustomerSignUpForm
from flask import redirect, render_template, request, url_for, Blueprint
from flask_login import login_required

accounts = Blueprint('accounts', __name__, template_folder='templates', static_url_path='static', url_prefix='/accounts')

@accounts.route('/retrieveAdminProfile')
@login_required
<<<<<<< HEAD
def retrieveAdminProfile():

    return render_template('accounts/retrieveAdminProfile.html')


# Admin Updates profile
@accounts.route('/updateAdminProfile/<int:id>/', methods=['GET', 'POST'])
def updateAdminProfile(id):
    update_customer_form = CustomerSignUpForm(request.form)
    if request.method == 'POST':
        customers_dict = {}
        db = shelve.open('tit/database/users.db', 'w')
        customers_dict = db['Customers']

        customer = customers_dict.get(id)
        customer.set_name(update_customer_form.name.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_phone_number(update_customer_form.phone_number.data)

        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('admin.accounts.retrieveAdminProfile'))
    else:
        customers_dict = {}
        db = shelve.open('tit/database/users.db', 'r')

        try:
           customers_dict = db['Customers']
        except:
           print("Error in retrieving customer profile from users.db.")

        customer = customers_dict.get(id)
        update_customer_form.name.data = customer.get_name()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.phone_number.data = customer.get_phone_number()

        db.close()

# PROMPT: CUSTOMER PROFILE HAS BEEN UPDATED
        return render_template('accounts/updateAdminProfile.html', form=update_customer_form)



# Admin - Retrieve Customers
@accounts.route('/retrieveCustomers')
@login_required
=======

def retrieveProfile():

    return render_template('accounts/retrieveAdminProfile.html')

# Admin - Retrieve Customers
@accounts.route('/retrieveCustomers')
>>>>>>> 8f69e118ce7bfd6896ba10a4436d3523d22270f7
def retrieveUsers():
    customers_list = []
    admins_list = []
    customers_dict = {}
    admin_dict = {}
    db = shelve.open('tit/database/users.db', 'r')
    try:
        customers_dict = db['Customers']
    except:
<<<<<<< HEAD
        print("Error in retrieving Customers from users.db.")
    try:
        admin_dict = db['Admins']
    except:
        print("Error in retrieving Admins from users.db.")
=======
        print("Error in retrieving Customers from customers.db.")
    try:
        admin_dict = db['Admins']
    except:
        print("Error in retrieving Admins from customers.db.")
>>>>>>> 8f69e118ce7bfd6896ba10a4436d3523d22270f7

    db.close()
    for customer in customers_dict.values():
        customers_list.append(customer)
    for admin in admin_dict.values():
        admins_list.append(admin)


    return render_template('accounts/retrieveCustomers.html', countCust=len(customers_list), cust_list=customers_list, countAdmin=len(admins_list), admins_list=admins_list)



# Admin Updates Customer profile
@accounts.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
<<<<<<< HEAD
@login_required
=======
>>>>>>> 8f69e118ce7bfd6896ba10a4436d3523d22270f7
def update_user(id):
    update_customer_form = CustomerSignUpForm(request.form)
    if request.method == 'POST':
        customers_dict = {}
        db = shelve.open('tit/database/users.db', 'w')
        customers_dict = db['Users']

        customer = customers_dict.get(id)
        customer.set_name(update_customer_form.name.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_phone_number(update_customer_form.phone_number.data)
        customer.set_password(update_customer_form.password.data)

        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('admin.accounts.retrieveUsers'))
    else:
        customers_dict = {}
        db = shelve.open('tit/database/users.db', 'r')

        try:
           customers_dict = db['Customers']
        except:
           print("Error in retrieving customer from users.db.")

        customers_dict = db['Customers']
        db.close()

        customer = customers_dict.get(id)
        update_customer_form.name.data = customer.get_name()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.phone_number.data = customer.get_phone_number()
        update_customer_form.password.data = customer.get_password()

# PROMPT: CUSTOMER PROFILE HAS BEEN UPDATED
        return render_template('accounts/updateCustomer.html', form=update_customer_form)


# Admin deletes customer
@accounts.route('/deleteCustomer/<int:id>', methods=['POST'])
<<<<<<< HEAD
@login_required
=======
>>>>>>> 8f69e118ce7bfd6896ba10a4436d3523d22270f7
def delete_user(id):
    customers_dict = {}
    db = shelve.open('tit/database/users.db', 'w')

    try: 
        customers_dict = db['Customers']
   
    except:
        print("Error in retrieving Customers from users.db.")

    # customers_dict = db['Customers']  

    customers_dict.pop(id)
    db['Customers'] = customers_dict
    db.close()

    return redirect(url_for('admin.accounts.retrieveUsers'))


# Admin Enter correct Password, then direct to change password page
@accounts.route('/retrieveAdminPW', methods=['GET','POST'])
@login_required
def retrieveAdminPW():
    admins_list = []
    admin_dict = {}
    change_password_form = ChangePasswordForm(request.form)  
    if request.method == 'POST':
        db = shelve.open('tit/database/users.db', 'r')
        try:
            admin_dict = db['Admins']
        except:
            print("Error in retrieving Admins from users.db.")
        db.close()
        for admin in admin_dict.values():
            admins_list.append(admin)
            if admin.get_password() == change_password_form.password.data:
                print('Customer keyed in the correct password.')
                # redirect to admin site.
                redirect(url_for("admin.accounts.updateAdminPW"))

            else:
                print('Admin failed to remember own password.')
    return render_template('accounts/retrieveAdminPW.html', form=change_password_form, admins_list=admins_list)


# Update/Change Password
@accounts.route('/updateAdminPW/<int:id>/', methods=['GET', 'POST'])
@login_required
def update_password(id):
    update_password_form = CustomerSignUpForm(request.form)
    if request.method == 'POST':
        customers_dict = {}
        db = shelve.open('users.db', 'w')
        customers_dict = db['Customers']

        customer = customers_dict.get(id)
        customer.set_password(update_password_form.password.data)
        customer.set_confirm_password(update_password_form.confirm_password.data)
        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('admin.accounts.retrieveAdminPW'))
    else:
        customers_dict = {}
        db = shelve.open('users.db', 'r')

        try:
           customers_dict = db['Customers']
        except:
           print("Error in retrieving customer profile from users.db.")

        customers_dict = db['Customers']
        db.close()

        customer = customers_dict.get(id)
        update_password_form.password.data = customer.get_password()
        update_password_form.confirm_password.data = customer.get_confirm_password()


        # PROMPT: CUSTOMER PROFILE HAS BEEN UPDATED
        return render_template('accounts/updateAdminPW.html', form=update_password_form)

