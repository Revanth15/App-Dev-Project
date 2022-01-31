from flask import Blueprint, render_template, redirect

from tit.admin.inventory.routes import inventory
from tit.admin.reporting.routes import reporting
from tit.admin.rewards.routes import rewards
from tit.admin.accounts.routes import accounts
from tit.admin.support.routes import support
admin = Blueprint('admin', __name__, url_prefix='/admin')

admin.register_blueprint(inventory)
admin.register_blueprint(reporting)
admin.register_blueprint(rewards)
admin.register_blueprint(accounts)
admin.register_blueprint(support)

@admin.route('/')
def adminRedirect():
    return redirect('/admin/dashboard')

@admin.route('/dashboard')
def dashboard():
    return render_template('admin_home.html')
