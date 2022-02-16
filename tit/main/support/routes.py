from flask import render_template, request, redirect, url_for, Blueprint
from tit.classes.Feedback import feedback
from tit.main.support.Forms import CreateFeedbackForm
import tit.classes.User as User
import shelve
from flask_login import current_user

from tit.utils import get_db, set_db


support = Blueprint('support', __name__, template_folder="templates", static_url_path="static", url_prefix="/support" )


@support.route('/ContactUs')
def Contact_Us():
    return render_template('support/ContactUs.html')


@support.route('/ContactInfo')
def Contact_Info():
    return render_template('support/ContactInfo.html')


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
        a,b = i.rstrip('\n').split('|')
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
        users_dict = get_db('feedback', 'Feedback')

        user = feedback(create_user_form.Name.data, create_user_form.email.data, create_user_form.type.data, create_user_form.feedback.data)
        if current_user.is_authenticated:
            user.set_id(current_user.get_id()) 

        users_dict[user.get_id()] = user
        set_db('feedback', 'Feedback', users_dict)

        # Test codes
        
       
        print(user.get_Name(),  "was stored in feedback.db successfully")

        return redirect(url_for('main.support.AfterSubmit'))
    return render_template('support/FeedbackPage.html', form=create_user_form)

@support.route('/AfterSubmit')
def AfterSubmit():
    return render_template('support/AfterSubmit.html')