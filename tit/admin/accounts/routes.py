import shelve
from tit.main.accounts.Forms import ChangePasswordForm, CustomerSignUpForm
from flask import redirect, render_template, request, url_for, Blueprint
from flask_login import login_required

from tit.utils import get_db, set_db

accounts = Blueprint('accounts', __name__, template_folder='templates', static_url_path='static', url_prefix='/accounts')

@accounts.route('/retrieveAdminProfile')
@login_required
def retrieveAdminProfile():

    return render_template('accounts/retrieveAdminProfile.html')


# Admin Updates profile
@accounts.route('/updateAdminProfile/<int:id>/', methods=['GET', 'POST'])
def updateAdminProfile(id):
    update_customer_form = CustomerSignUpForm(request.form)
    customers_dict = get_db('users', 'Customers')
    if request.method == 'POST':

        customer = customers_dict.get(id)
        customer.set_name(update_customer_form.name.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_phone_number(update_customer_form.phone_number.data)

        set_db('users', 'Customers', customers_dict)

        return redirect(url_for('admin.accounts.retrieveAdminProfile'))
    else:
        customer = customers_dict.get(id)
        update_customer_form.name.data = customer.get_name()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.phone_number.data = customer.get_phone_number()
# PROMPT: CUSTOMER PROFILE HAS BEEN UPDATED
        return render_template('accounts/updateAdminProfile.html', form=update_customer_form)



# Admin - Retrieve Customers
@accounts.route('/retrieveUsers')
@login_required
def retrieveUsers():
    customers_list = []
    admins_list = []
    customers_dict = get_db('users', 'Customers')
    admin_dict = get_db('users', 'Admins')

    for customer in customers_dict.values():
        customers_list.append(customer)
    for admin in admin_dict.values():
        admins_list.append(admin)


    return render_template('accounts/retrieveCustomers.html', countCust=len(customers_list), cust_list=customers_list, countAdmin=len(admins_list), admins_list=admins_list)



# Admin Updates User profile
@accounts.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
@login_required
def update_customer(id):
    update_customer_form = CustomerSignUpForm(request.form)
    customers_dict = get_db('users', 'Customers')
    if request.method == 'POST':
        customer = customers_dict.get(id)
        customer.set_name(update_customer_form.name.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_phone_number(update_customer_form.phone_number.data)
        customer.set_password(update_customer_form.password.data)

        customers_dict[id] = customer
        set_db('users', 'Customers', customers_dict)

        return redirect(url_for('admin.accounts.retrieveUsers'))
    else:
        customer = customers_dict.get(id)
        update_customer_form.name.data = customer.get_name()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.phone_number.data = customer.get_phone_number()
        update_customer_form.password.data = customer.get_password()

# PROMPT: CUSTOMER PROFILE HAS BEEN UPDATED
        return render_template('accounts/updateCustomer.html', form=update_customer_form)


# Admin Updates Admin profile
@accounts.route('/updateAdmin/<int:id>/', methods=['GET', 'POST'])
@login_required
def update_admin(id):
    update_customer_form = CustomerSignUpForm(request.form)
    admins_dict = get_db('users', 'Admins')
    if request.method == 'POST':
        admin = admins_dict.get(id)
        admin.set_name(update_customer_form.name.data)
        admin.set_email(update_customer_form.email.data)
        admin.set_gender(update_customer_form.gender.data)
        admin.set_phone_number(update_customer_form.phone_number.data)
        admin.set_password(update_customer_form.password.data)

        admins_dict[id] = admin
        set_db('users', 'Admins', admins_dict)

        return redirect(url_for('admin.accounts.retrieveUsers'))
    else:
        admin = admins_dict.get(id)
        update_customer_form.name.data = admin.get_name()
        update_customer_form.email.data = admin.get_email()
        update_customer_form.gender.data = admin.get_gender()
        update_customer_form.phone_number.data = admin.get_phone_number()
        update_customer_form.password.data = admin.get_password()

# PROMPT: CUSTOMER PROFILE HAS BEEN UPDATED
        return render_template('accounts/updateCustomer.html', form=update_customer_form)



# Admin deletes Customers
@accounts.route('/deleteCustomer/<int:id>', methods=['POST'])
@login_required
def delete_customer(id):
    customers_dict = get_db('users', 'Customers')
    customers_dict.pop(id)
    set_db('users', 'Customers', customers_dict)
    print('Customer Deleted!')

    return redirect(url_for('admin.accounts.retrieveUsers'))


@accounts.route('/deleteAdmin/<int:id>', methods=['POST'])
@login_required
def delete_admin(id):
    admins_dict = get_db('users', 'Admins')
    admins_dict.pop(id)
    set_db('users', 'Admins', admins_dict)
    print('Admins Deleted!')

    notifications_dict = get_db('notification', 'Notifications')
    for notif in notifications_dict.values():
        if id in notif.get_seenby():
            notif.delete_seenby(id)
    set_db('notification', 'Notifications', notifications_dict)

    return redirect(url_for('admin.accounts.retrieveUsers'))


# Admin Enter correct Password, then direct to change password page
@accounts.route('/retrieveAdminPW', methods=['GET','POST'])
@login_required
def retrieveAdminPW():
    admins_list = []
    admin_dict = get_db('users', 'Admins')
    change_password_form = ChangePasswordForm(request.form)  
    if request.method == 'POST':
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
    customers_dict = get_db('users', 'Customers')
    if request.method == 'POST':
        customer = customers_dict.get(id)
        customer.set_password(update_password_form.password.data)
        customer.set_confirm_password(update_password_form.confirm_password.data)

        set_db('users', 'Customers', customers_dict)


        return redirect(url_for('admin.accounts.retrieveAdminPW'))
    else:
        customer = customers_dict.get(id)
        update_password_form.password.data = customer.get_password()
        update_password_form.confirm_password.data = customer.get_confirm_password()


        # PROMPT: CUSTOMER PROFILE HAS BEEN UPDATED
        return render_template('accounts/updateAdminPW.html', form=update_password_form)

