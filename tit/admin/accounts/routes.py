import shelve
from tit.main.accounts.Forms import CustomerSignUpForm
from flask import redirect, render_template, request, url_for, Blueprint

accounts = Blueprint('accounts', __name__, template_folder='templates', static_url_path='static', url_prefix='/accounts')


# Admin - Retrieve Customers
@accounts.route('/retrieveCustomers')
def retrieveCustomers():
    customers_dict = {}
    db = shelve.open('customers.db', 'r')

    try:
        customers_dict = db['Customers']
    except:
        print("Error in retrieving Customers from storage.db.")

    customers_dict = db['Customers']
    print(db['Customers'])
    db.close()

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)

    return render_template('retrieveCustomers.html', count=len(customers_list), customers_list=customers_list)



# Admin Updates Customer profile
@accounts.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    update_customer_form = CustomerSignUpForm(request.form)
    if request.method == 'POST':
        customers_dict = {}
        db = shelve.open('customers.db', 'w')
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

        return redirect(url_for('admin.accounts.retrieveCustomers'))
    else:
        customers_dict = {}
        db = shelve.open('customers.db', 'r')

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
        return render_template('updateCustomer.html', form=update_customer_form)


# Admin deletes customer
@accounts.route('/deleteCustomer/<int:id>', methods=['POST'])
def delete_customer(id):
    customers_dict = {}
    db = shelve.open('customers.db', 'w')

    try: 
        customers_dict = db['Customers']
   
    except:
        print("Error in retrieving Customers from customers.db.")

    # customers_dict = db['Customers']  

    customers_dict.pop(id)
    db['Customers'] = customers_dict
    db.close()

    return redirect(url_for('admin.accounts.retrieveCustomers'))