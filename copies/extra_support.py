#from crypt import methods
from flask import Flask, render_template, request, redirect, url_for
from tit.main.support.Forms import CreateFeedbackForm
import tit.classes.User as User, tit.classes.accountFAQ as accountFAQ
import email_validator
import shelve

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('base.html')

@app.route('/ContactUs')
def Contact_Us():
    return render_template('ContactUs.html')


@app.route('/ContactInfo')
def Contact_Info():
    return render_template('ContactInfo.html')

@app.route('/FAQ_GS')
def FAQ_GS():
    question = {}
    
    db = open('FAQ_GettingStarted.txt')
    
    for i in db:
        a,b = i.rstrip('\n').split('|')
        question[str(a)] = str(b)
        
        
        
    db.close()
    return render_template('FAQ.html', question=question)

@app.route('/FAQ_MA')
def FAQ_MA():
    question = {}
    
    db = open('FAQ_MyAccount.txt')
    
    for i in db:
        a,b = i.rstrip('\n').split('|')
        question[str(a)] = str(b)
        
        
        
    db.close()
    return render_template('FAQ.html', question=question)

@app.route('/FAQ_PAS')
def FAQ_PAS():
    question = {}
    
    db = open('FAQ_Payment&Shipping.txt')
    
    for i in db:
        a,b = i.rstrip('\n').split('|')
        question[str(a)] = str(b)
        
        
        
    db.close()
    return render_template('FAQ.html', question=question)

@app.route('/FAQ_RAO')
def FAQ_RAO():
    question = {}
    
    db = open('FAQ_RewardsAndOffers.txt')
    
    for i in db:
        a,b = i.rstrip('\n').split('|')
        question[str(a)] = str(b)
        
        
        
    db.close()
    return render_template('FAQ.html', question=question)

@app.route('/FAQ_T')
def FAQ_T():
    question = {}
    
    db = open('FAQ_Troubleshooting.txt')
    
    for i in db:
        a,b = i.rstrip('\n').split(',')
        question[str(a)] = str(b)
        
        
        
    db.close()
    return render_template('FAQ.html', question=question)

@app.route('/FAQ_OS')
def FAQ_OS():
    question = {}
    
    db = open('FAQ_OtherSupport.txt')
    
    for i in db:
        a,b = i.rstrip('\n').split('|')
        question[str(a)] = str(b)
        
        
        
    db.close()
    return render_template('FAQ.html', question=question)


           

@app.route('/FeedbackPage', methods=['GET', 'POST'])
def create_user():
    create_user_form = CreateFeedbackForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")

        user = User.User(create_user_form.first_name.data, create_user_form.last_name.data, create_user_form.email.data, create_user_form.feedback.data)
        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict

        # Test codes
        users_dict = db['Users']
        user = users_dict[user.get_user_id()]
        print(user.get_first_name(), user.get_last_name(), "was stored in user.db successfully with user_id ==", user.get_user_id())

        db.close()

        return redirect(url_for('AfterSubmit'))
    return render_template('FeedbackPage.html', form=create_user_form)


@app.route('/AdminFeedbackPage')
def retrieve_users():
    users_dict = {}
    db = shelve.open('user.db', 'r')
    try:
        users_dict = db['Users']
    except:
        print("Error in retrieving users from user.db.")

    db.close()
    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('AdminFeedbackPage.html', count=len(users_list), users_list=users_list)


@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
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


        return redirect(url_for('retrieve_users'))
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
        return render_template('updateUser.html', form=update_user_form)

@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('user.db', 'w')
    users_dict = db['Users']

    users_dict.pop(id)

    db['Users'] = users_dict
    db.close()

    return redirect(url_for('retrieve_users'))

@app.route('/AfterSubmit')
def AfterSubmit():
    return render_template('AfterSubmit.html')



    




if __name__ == "__main__":
    app.run(debug=True)
