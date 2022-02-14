from flask import Blueprint, render_template, redirect, url_for, g, request, abort

import json
import datetime

from tit import app
from tit.admin.inventory.routes import inventory
from tit.admin.reporting.routes import reporting
from tit.admin.reporting.utils import db_count_occurence, db_get_qty
from tit.admin.rewards.routes import rewards
from tit.admin.accounts.routes import accounts
from tit.admin.support.routes import support
from tit.admin.reporting.Forms import createURLMapForm

from tit.utils import get_db, set_db, dbkeys
from flask_login import current_user, login_required

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
    
@admin.before_request
@login_required
def authorize():
    if current_user.get_role() != 'Admin':
        abort(404)


@admin.route('/')
def adminRedirect():
    return redirect('/admin/dashboard')

@admin.route('/dashboard')
def dashboard():
    dashboard_list = []

    #* Traffic Count
    sessions_dict = get_db('traffic', 'Sessions')
    user_list = []
    for session in sessions_dict.values():
        if type(session.get_views()[-1][1]) == str:
            view_date = datetime.datetime.strptime(session.get_views()[-1][1], '%Y-%m-%d, %H:%M:%S').date()
        else:
            view_date = session.get_views()[-1][1].date()
        if view_date == datetime.date.today():
            user_list.append(session)

    # Format data for Dashboard
    data = [['Session ID', 'IP Address', 'Time', 'Last View'], []]
    for user in user_list:
        user_data = [user.get_session(), user.get_ip(), user.get_created(), user.get_views()[-1][0]]
        data[1].append(user_data)
    visitor_card = ['Visitors Today', len(data[1]), data]
    dashboard_list.append(visitor_card)


    #*SignUp Count
    accounts_dict = get_db('users', 'Customers')
    signups_list = []
    for user in accounts_dict.values():
        signupdate = user.get_created('date', 'obj')
        if signupdate == datetime.date.today():
            signups_list.append(user)

    # Format data for Dashboard
    data = [['User ID', 'Name', 'Email', 'Time'], []]
    for user in signups_list:
        user_data = [user.get_id(), user.get_name(), user.get_email(), user.get_created()]
        data[1].append(user_data)
    signup_data = ['New Sign Ups Today', len(data[1]), data]
    dashboard_list.append(signup_data)


    #* Support Count
    feedback_dict = get_db('feedback', 'Feedback')
    feedback_list = []
    for feedback in feedback_dict.values():
        feedbackdate = feedback.get_created('date', 'obj')
        if feedbackdate == datetime.date.today():
            feedback_list.append(feedback)


    # Format data for Dashboard
    data = [['ID', 'Name', 'Time'], []]
    for user in feedback_list:
        user_data = [user.get_id(), user.get_Name(), user.get_created()]
        data[1].append(user_data)
    feedback_data = ['Feedback Today', len(data[1]), data]
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
    # data = []
    # data.append(db_count_occurence('traffic', 'Sessions', 'get_created', '%m-%d'))
    # data.append(db_get_qty('products', 'products', 'get_quantity'))
    # data.append(get_db('archive', 'Archives', 'get_created', '%m-%d'))
    return render_template('dashboard.html', cards = dashboard_list, data=data)




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