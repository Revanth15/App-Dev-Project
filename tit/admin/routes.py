from flask import Blueprint, render_template, redirect, url_for, g, request, abort

import json

from tit import app
from tit.admin.inventory.routes import inventory
from tit.admin.reporting.routes import reporting
from tit.admin.rewards.routes import rewards
from tit.admin.accounts.routes import accounts
from tit.admin.support.routes import support

from tit.utils import get_db, set_db
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
    return render_template('dashboard.html')

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
    file = open('index.txt', 'r')
    index = file.read()
    file.close()
    index = json.loads(index)
    if request.method == 'POST':
        for rule in app.url_map.iter_rules():
            if rule.__str__() not in index:
                rule_dict = {}
                for method in rule.methods:
                    if method == 'GET':
                        rule_dict.update({method:'view'})
                    elif method == 'POST':
                        rule_dict.update({method:''})
                index.update({rule.__str__():rule_dict})
    
    return render_template('')