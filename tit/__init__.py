import shelve
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_recaptcha import ReCaptcha
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from tit.main.accounts.Forms import LoginForm
from tit.utils import get_db

app = Flask(__name__)
app.config.from_object('config')
recaptcha = ReCaptcha(app)
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

# @app.before_request
# def print_user():
#     print(current_user.get_id())
#     print(current_user.get_role())

@login_manager.user_loader
def load_user(user_id):
    user_list = []
    customers_dict = get_db('users', 'Customers')
    admin_dict = get_db('users', 'Admins')


    for customer in customers_dict.values():
        user_list.append(customer)
    for admin in admin_dict.values():
        user_list.append(admin)
    for user in user_list:
        if user.get_id() == user_id:

    # given id, return customer object

            if user:
                return user


@app.route('/login', methods=['GET','POST'])
def login():
    login_form = LoginForm(request.form)

    if request.method == 'POST':
        if 'admin@tit.com' in login_form.email.data:
            users_dict = get_db('users', 'Admins')

        else:
            users_dict = get_db('users', 'Customers')

        print(login_form.email.data)  
        print(login_form.password.data)
        for user in users_dict.values():
            if 'admin@tit.com' in login_form.email.data:
                print('yes')
                if user.get_password() == login_form.password.data:
                    login_user(user)
                    print("Admin login successful")
                    flash('You have been logged in', 'success')
                    return(redirect(url_for("admin.dashboard")))
            else:
                if user.get_email() == login_form.email.data:
                    if user.get_password() == login_form.password.data:
                        login_user(user, remember=login_form.remember.data)
                        print('Customer login successful')
                        flash('Login Successful')

                        # add a next page route
                        next_page = request.args.get('next')
                        print(next_page)
                        return redirect(next_page) if next_page else redirect(url_for("main.home"))

        flash('Incorrect email or password.')
    return render_template('login.html', form=login_form)


# Customer Logout 
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404

