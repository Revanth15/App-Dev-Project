import shelve
from flask import Flask, render_template
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object('config')
bcrypt = Bcrypt(app)
# we add functionality to db models, it will handle sessions in the background
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from tit.admin.routes import admin
from tit.main.routes import main

app.register_blueprint(admin)
app.register_blueprint(main)

@login_manager.user_loader
def load_user(customer_id):
    customers_dict = {}
    db = shelve.open('customers.db', 'c')
    try:

        customers_dict = db['Customers']
    except:
        print("Error in retrieving Customers from customers.db.")
    # given id, return customer object
    customer = customers_dict.get(customer_id)
    db.close()
    if customer:
        return customer


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404