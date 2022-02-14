from flask import render_template, request, redirect, url_for, Blueprint
from tit.main.support.Forms import CreateFeedbackForm
import shelve

support = Blueprint('support', __name__, template_folder="templates", static_url_path="static", url_prefix="/support" )


@support.route('/AdminFeedbackPage')
def AdminFeedbackPage():
    users_dict = {}
    db = shelve.open('tit/database/feedback.db', 'r')
    try:
        users_dict = db['Feedback']
    except:
        print("Error in retrieving users from feedback.db.")

    db.close()
    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('support/AdminFeedbackPage.html', count=len(users_list), users_list=users_list)


@support.route('/updateUser/<id>/', methods=['GET', 'POST'])
def update_user(id):

    update_user_form = CreateFeedbackForm(request.form)

    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('tit/database/feedback.db', 'w')
        users_dict = db['Feedback']

        user = users_dict.get(id)
        user.set_Name(update_user_form.Name.data)
        user.set_email(update_user_form.email.data)
        user.set_type(update_user_form.type.data)
        user.set_feedback(update_user_form.feedback.data)
        user.set_status(update_user_form.status.data)

        db['Feedback'] = users_dict
        db.close()


        return redirect(url_for('admin.support.AdminFeedbackPage'))
    else:
        users_dict = {}
        db = shelve.open('tit/database/feedback.db', 'r')
        users_dict = db['Feedback']
        db.close()

        user = users_dict.get(id)
        update_user_form.Name.data = user.get_Name()
        update_user_form.email.data = user.get_email()
        update_user_form.type.data = user.get_type()
        update_user_form.feedback.data = user.get_feedback()
        update_user_form.status.data = user.get_status()

        return render_template('support/updateUser.html', form=update_user_form)

@support.route('/deleteUser/<id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('tit/database/feedback.db', 'w')
    users_dict = db['Feedback']

    users_dict.pop(id)

    db['Feedback'] = users_dict
    db.close()

    return redirect(url_for('admin.support.AdminFeedbackPage'))