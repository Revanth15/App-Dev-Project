import datetime
from flask import Blueprint, render_template, redirect, session, url_for, g, request

import json

import werkzeug

from tit import app
from tit.admin.inventory.routes import inventory
from tit.admin.reporting.routes import reporting
from tit.admin.rewards.routes import rewards
from tit.admin.accounts.routes import accounts
from tit.admin.support.routes import support
from tit.admin.reporting.Forms import createURLMapForm

from tit.utils import dbkeys, get_db, set_db
from flask_login import current_user
admin = Blueprint('admin', __name__, url_prefix='/admin')

admin.register_blueprint(inventory)
admin.register_blueprint(reporting)
admin.register_blueprint(rewards)
admin.register_blueprint(accounts)
admin.register_blueprint(support)

@admin.before_request
def get_notifications():
    notif_dict = get_db('notification', 'Notifications')
    notif_list = notif_dict.values()
    g.notif_list = notif_list
    


@admin.route('/')
def adminRedirect():
    return redirect('/admin/dashboard')

@admin.route('/dashboard')
def dashboard():
    dashboard_list = []

    #* Traffic Count
    sessions_dict = get_db('traffic', 'Sessions')
    user_list = []
    for user in sessions_dict.values():
        view_date = datetime.datetime.strptime(user.get_created(), '%Y-%m-%d %H:%M:%S').date()
        if view_date == datetime.datetime.now().date():
            user_list.append(user)

    # Format data for Dashboard
    data = []
    for user in user_list:
        user_data = {
        'Session ID': user.get_session(),
        'IP Address': user.get_ip(),
        'Time': user.get_created(),
        'Last View': user.get_views()[-1][0]
        }
        data.append(user_data)
    visitor_card = ['Visitors Today', len(data), data]
    dashboard_list.append(visitor_card)


    #*SignUp Count
    accounts_dict = get_db('customers', 'Customers')
    signups_list = []
    for user in accounts_dict.values():
        signupdate = user.get_created('date', 'obj')
        if signupdate == datetime.date.today():
            signups_list.append(user)

    # Format data for Dashboard
    data = []
    for user in signups_list:
        user_data = {
        'User ID': user.get_id(),
        'Name': user.get_name(),
        'Email': user.get_email(),
        'Time': user.get_created()
        }
        data.append(user_data)
    print(data)
    signup_data = ['New Sign Ups Today', len(data), data]
    dashboard_list.append(signup_data)


    #* Support Count
    feedback_dict = get_db('user', 'Users')
    feedback_list = []
    for feedback in feedback_dict.values():
        feedbackdate = feedback.get_created('date', 'obj')
        if feedbackdate == datetime.date.today():
            feedback_list.append(feedback)


    # Format data for Dashboard
    data = []
    for user in feedback_list:
        user_data = {
        'User ID': user.get_id(),
        'Name': user.get_name(),
        'Time': user.get_created()
        }
        data.append(user_data)
    feedback_data = ['Feedback Today', len(data), data]
    dashboard_list.append(feedback_data)


    #* Sales Count
    # sales_dict = get_db('user', 'Users')
    # sales_list = []
    # for sale in sales_dict.values():
    #     saledate = sale.get_created('date', 'obj')
    #     if saledate == datetime.date.today():
    #         sales_list.append(sale)


    # # Format data for Dashboard
    # data = []
    # for sale in sales_list:
    #     sale_data = {
    #     'Order ID': user.get_id(),
    #     '': user.get_name(),
    #     'Time': user.get_created()
    #     }
    #     data.append(sale_data)
    # sales_data = ['Feedback Today', len(data), data]
    # dashboard_list.append(sales_data)

    return render_template('dashboard.html', cards = dashboard_list)




@admin.route('/opennotif/<id>')
def opennotif(id):
    notification_dict = get_db('notification', 'Notifications')
    notif = notification_dict[id]
    notif.update_seenby(current_user.get_id())
    notification_dict[id] = notif
    set_db('notification', 'Notifications', notification_dict)
    return redirect(url_for(f'admin.{notif.get_url()}'))

@admin.route('/updateURLMap', methods=['GET', 'POST'])
def update_url_map():
    file = open('index.json', 'r')
    index = json.load(file)
    file.close()

    for rule in app.url_map.iter_rules():
        route = rule.__str__()
        if 'admin' not in route:
            if route not in index:
                rule_dict = {}
                for method in rule.methods:
                    if method == 'GET':
                        rule_dict.update({method:'view'})
                    elif method == 'POST':
                        rule_dict.update({method:''})
                index.update({route:rule_dict})

    for rule in index.copy():
        if 'admin' in rule:
            index.pop(rule)
    rule_list = []
    form_data = []
    for rule in index:
        if index[rule].get('POST') is not None:
            rule_list.append(rule)
            form_data.append(index[rule].get('POST'))
    print(form_data)
    form = createURLMapForm(rule_list, request.form)



    if request.method == 'POST' and form.validate():
        for field in form:
           index.get(field.name)['POST']=field.data
        file = open('index.json', 'w')
        json.dump(index, file)
        file.close()
        return redirect(url_for('admin.update_url_map'))

    for field, data in zip(form,form_data):
        field.data = data
    
    return render_template('updateURLmap.html', form =form, form_data=form_data)