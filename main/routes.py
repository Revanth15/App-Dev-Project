from flask import render_template, Blueprint

from tit.main.accounts.routes import accounts

main = Blueprint('main', __name__)

main.register_blueprint(accounts)

@main.route('/')
def home():
    return render_template('base.html')


