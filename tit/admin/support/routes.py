from flask import render_template, request, redirect, url_for, Blueprint
from tit.main.support.Forms import CreateFeedbackForm
import shelve

support = Blueprint('support', __name__, template_folder="templates", static_url_path="static", url_prefix="/support" )


@support.route('/AdminFeedbackPage')
def retrieve_users():
    users_dict = {}
    db = shelve.open('tit/database/user.db', 'r')
    try:
        users_dict = db['Users']
    except:
        print("Error in retrieving users from user.db.")

    db.close()
    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('support/AdminFeedbackPage.html', count=len(users_list), users_list=users_list)


@support.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):

    update_user_form = CreateFeedbackForm(request.form)

    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_first_name(update_user_form.first_name.data)
        user.set_last_name(update_user_form.last_name.data)
        user.set_email(update_user_form.email.data)
        user.set_feedback(update_user_form.feedback.data)

        db['Users'] = users_dict
        db.close()


        return redirect(url_for('admin.support.retrieve_users'))
    else:
        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(id)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.email.data = user.get_email()
        update_user_form.feedback.data = user.get_feedback()
        return render_template('support/updateUser.html', form=update_user_form)

@support.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('user.db', 'w')
    users_dict = db['Users']

    users_dict.pop(id)

    db['Users'] = users_dict
    db.close()

    return redirect(url_for('admin.support.retrieve_users'))