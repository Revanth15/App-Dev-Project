from flask import render_template, Blueprint

from tit.admin.accounts.routes import accounts
admin = Blueprint('admin', __name__, url_prefix='/admin')

admin.register_blueprint(accounts)


@admin.route('/admin_home')
def admin_home():
    return render_template('admin_home.html')

