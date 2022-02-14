import shelve
from tit.main.accounts.Forms import ChangePasswordForm, CustomerSignUpForm
from flask import redirect, render_template, request, url_for, Blueprint
from flask_login import login_required

accounts = Blueprint('accounts', __name__, template_folder='templates', static_url_path='static', url_prefix='/accounts')

@accounts.route('/retrieveAdminProfile')
@login_required

def retrieveProfile():

    return render_template('accounts/retrieveAdminProfile.html')

# Admin - Retrieve Customers
@accounts.route('/retrieveCustomers')
def retrieveUsers():
    customers_list = []
    admins_list = []
    customers_dict = {}
    admin_dict = {}
    db = shelve.open('tit/database/users.db', 'r')
    try:
        customers_dict = db['Customers']
    except:
        print("Error in retrieving Customers from customers.db.")
    try:
        admin_dict = db['Admins']
    except:
        print("Error in retrieving Admins from customers.db.")

    db.close()
    for customer in customers_dict.values():
        customers_list.append(customer)
    for admin in admin_dict.values():
        admins_list.append(admin)


    return render_template('accounts/retrieveCustomers.html', countCust=len(customers_list), cust_list=customers_list, countAdmin=len(admins_list), admins_list=admins_list)



# Admin Updates Customer profile
@accounts.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
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
        customer.set_password(update_customer_form.password.data)

        # user.set_first_name(update_user_form.first_name.data)
        # user.set_last_name(update_user_form.last_name.data)
        # user.set_address(update_user_form.address.data)
        # user.set_postal_code(update_user_form.postal_code.data)
        # user.set_unit_number(update_user_form.unit_number.data)

        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('admin.accounts.retrieveUsers'))
    else:
        customers_dict = {}
        db = shelve.open('tit/database/customers.db', 'r')

        try:
           customers_dict = db['Customers']
        except:
           print("Error in retrieving customer from customers.db.")

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
def delete_user(id):
    customers_dict = {}
    db = shelve.open('tit/database/customers.db', 'w')

    try: 
        customers_dict = db['Customers']
   
    except:
        print("Error in retrieving Customers from customers.db.")

    # customers_dict = db['Customers']  

    customers_dict.pop(id)
    db['Customers'] = customers_dict
    db.close()

    return redirect(url_for('admin.accounts.retrieveUsers'))

    

# Admin Enter correct Password, then direct to change password page
@accounts.route('/currentAdminPW', methods=['GET','POST'])
def currentAdminPW():
    change_password_form = ChangePasswordForm(request.form)  
    if request.method == 'POST':
    # if change_password_form.password.data == 'adminTime':
    #     flash("Type in yur new password.")
        customers_dict = {}
        db = shelve.open('customers.db', 'r')
        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving Customers' password from customers.db.")   
        db.close()
        for customer in customers_dict.values():
            customer.get_email() == 'admin@tit.com'
            if customer.get_password() == change_password_form.password.data:
                print('Customer keyed in the correct password.')
                # redirect to admin site.
                redirect(url_for("updatePassword/<int:id>/"))

            else:
                print('Admin failed to remember own password.')

        # return redirect(url_for('updatePassword/<int:id>/'))
        return redirect(url_for('updateAdminPW/<int:id>/'))
    return render_template('currentAdminPW.html', form=change_password_form)


# Update/Change Password
@accounts.route('/updateAdminPW/<int:id>/', methods=['GET', 'POST'])
def update_password(id):
    update_password_form = CustomerSignUpForm(request.form)
    if request.method == 'POST':
        customers_dict = {}
        db = shelve.open('customers.db', 'w')
        customers_dict = db['Customers']

        customer = customers_dict.get(id)
        customer.set_password(update_password_form.password.data)
        customer.set_confirm_password(update_password_form.confirm_password.data)
        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('retrievePassword'))
    else:
        customers_dict = {}
        db = shelve.open('customers.db', 'r')

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
        return render_template('updateAdminPW.html', form=update_password_form)

