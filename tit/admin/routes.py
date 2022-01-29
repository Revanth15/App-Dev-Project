from flask import Blueprint, render_template, redirect

from tit.admin.inventory.routes import inventory
from tit.admin.reporting.routes import reporting
admin = Blueprint('admin', __name__, url_prefix='/admin')

admin.register_blueprint(inventory)
admin.register_blueprint(reporting)

@admin.route('/')
def adminRedirect():
    return redirect('/admin/dashboard')

@admin.route('/dashboard')
def dashboard():
    return render_template('admin_home.html')
