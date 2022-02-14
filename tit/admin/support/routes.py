from flask import render_template, request, redirect, url_for, Blueprint
from tit.main.support.Forms import CreateFeedbackForm
import shelve

from tit.utils import get_db, set_db

support = Blueprint('support', __name__, template_folder="templates", static_url_path="static", url_prefix="/support" )


@support.route('/AdminFeedbackPage')
def AdminFeedbackPage():
    users_dict = get_db('feedback', 'Feedback')
    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('support/AdminFeedbackPage.html', count=len(users_list), users_list=users_list)


@support.route('/updateUser/<id>/', methods=['GET', 'POST'])
def update_user(id):
    users_dict = get_db('feedback', 'Feedback')
    update_user_form = CreateFeedbackForm(request.form)

    if request.method == 'POST' and update_user_form.validate():

        user = users_dict.get(id)
        user.set_Name(update_user_form.Name.data)
        user.set_email(update_user_form.email.data)
        user.set_type(update_user_form.type.data)
        user.set_feedback(update_user_form.feedback.data)
        user.set_status(update_user_form.status.data)

        set_db('feedback', 'Feedback', users_dict)


        return redirect(url_for('admin.support.AdminFeedbackPage'))
    else:
        user = users_dict.get(id)
        update_user_form.Name.data = user.get_Name()
        update_user_form.email.data = user.get_email()
        update_user_form.type.data = user.get_type()
        update_user_form.feedback.data = user.get_feedback()
        update_user_form.status.data = user.get_status()

        return render_template('support/updateUser.html', form=update_user_form)

@support.route('/deleteUser/<id>', methods=['POST'])
def delete_user(id):
    users_dict = get_db('feedback', 'Feedback')
    users_dict.pop(id)

    set_db('feedback', 'Feedback', users_dict)

    return redirect(url_for('admin.support.AdminFeedbackPage'))