from flask import render_template, request, redirect, url_for, Blueprint
from tit.main.support.Forms import CreateFeedbackForm
import tit.classes.User as User
import shelve

support = Blueprint('support', __name__, template_folder="templates", static_url_path="static", url_prefix="/support" )


@support.route('/FAQ_GS')
def FAQ_GS():
    question = {}
    
    db = open('tit/database/FAQ/FAQ_GettingStarted.txt')
    
    for i in db:
        a,b = i.rstrip('\n').split('|')
        question[str(a)] = str(b)
        
        
        
    db.close()
    return render_template('support/FAQ.html', question=question)

@support.route('/FAQ_MA')
def FAQ_MA():
    question = {}
    
    db = open('tit/database/FAQ/FAQ_MyAccount.txt')
    
    for i in db:
        a,b = i.rstrip('\n').split('|')
        question[str(a)] = str(b)
        
        
        
    db.close()
    return render_template('support/FAQ.html', question=question)

@support.route('/FAQ_PAS')
def FAQ_PAS():
    question = {}
    
    db = open('tit/database/FAQ/FAQ_Payment&Shipping.txt')
    
    for i in db:
        a,b = i.rstrip('\n').split('|')
        question[str(a)] = str(b)
        
        
        
    db.close()
    return render_template('support/FAQ.html', question=question)

@support.route('/FAQ_RAO')
def FAQ_RAO():
    question = {}
    
    db = open('tit/database/FAQ/FAQ_RewardsAndOffers.txt')
    
    for i in db:
        a,b = i.rstrip('\n').split('|')
        question[str(a)] = str(b)
        
        
        
    db.close()
    return render_template('support/FAQ.html', question=question)

@support.route('/FAQ_T')
def FAQ_T():
    question = {}
    
    db = open('tit/database/FAQ/FAQ_Troubleshooting.txt')
    
    for i in db:
        a,b = i.rstrip('\n').split(',')
        question[str(a)] = str(b)
        
        
        
    db.close()
    return render_template('support/FAQ.html', question=question)

@support.route('/FAQ_OS')
def FAQ_OS():
    question = {}
    
    db = open('tit/database/FAQ/FAQ_OtherSupport.txt')
    
    for i in db:
        a,b = i.rstrip('\n').split('|')
        question[str(a)] = str(b)
        
        
        
    db.close()
    return render_template('support/FAQ.html', question=question)


           

@support.route('/FeedbackPage', methods=['GET', 'POST'])
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

        return redirect(url_for('main.support.AfterSubmit'))
    return render_template('support/FeedbackPage.html', form=create_user_form)

@support.route('/AfterSubmit')
def AfterSubmit():
    return render_template('support/AfterSubmit.html')