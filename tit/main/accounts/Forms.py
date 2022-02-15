from flask import flash
from flask_login import current_user
from pyparsing import Regex
from wtforms import StringField, BooleanField, SelectField, validators, PasswordField, IntegerField, TextAreaField, RadioField, EmailField, TelField, Form
from wtforms.validators import Email
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError
from password_strength import PasswordPolicy, PasswordStats

from tit.classes.Customer import Customer
# from wtforms.fields.html5 import EmailField, DateField

# from flask import Flask, render_template, request, redirect, url_for, flash, session

def validate_email(form,field):
    email = field.data
    print(email)
    email_end = email.split('@')[-1]
    print(email_end)
    if email_end != 'gmail.com' and email_end != 'yahoo.com' and email_end != 'tit.com':
        print('error')
        raise ValidationError('Please enter a valid gmail/yahoo mail')


class CustomerSignUpForm(FlaskForm):
    name = StringField('Name(as in ID)', [validators.Length(min=1, max=30), validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired(), validators.Email(), validate_email])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    phone_number = StringField('Phone Number', [validators.Length(min=8, max=8), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm_password', message='Passwords do not match'), validators.Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", message='Weak Password')])
    confirm_password = PasswordField('Confirm Password', [validators.DataRequired(),validators.EqualTo('password', message='Passwords do not match')])


class LoginForm(FlaskForm):
    
    email = StringField('Email', [validators.DataRequired(), Email()])
    password = PasswordField('Password', [validators.DataRequired()])
    remember = BooleanField('Remember Me')
    
class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', [validators.DataRequired()])
    new_password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm_new_password', message='Passwords do not match')])
    confirm_password = PasswordField('Confirm New Password', [validators.DataRequired(),validators.EqualTo('new_password', message='Passwords do not match')])
    remember = BooleanField('Remember Me')

class getOTPForm(FlaskForm):
    phone_number = StringField('Phone Number', [validators.Length(min=8, max=8), validators.DataRequired()])



class ResetRequestForm():
    email = StringField('Email', [validators.Length(min=6, max=50), validators.DataRequired()])

class AdminCreateCustomer(FlaskForm):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    phone_number = IntegerField('Phone Number', [validators.NumberRange(min=8, max=8), validators.DataRequired()])
    Address = StringField('Address', [validators.Length(min=1, max=150), validators.DataRequired()])
    unit_number = StringField('Unit Number', [validators.Length(min=1, max=10), validators.DataRequired()])
    postal_code = IntegerField('Postal Code', [validators.Length(min=6, max=6), validators.DataRequired()])
    password = StringField('Password', [validators.Length(min=8, max=10), validators.DataRequired()])

#   membership = RadioField('Membership', choices=[('F', 'Fellow'), ('S', 'Senior'), ('P', 'Professional')], default='F')
#   remarks = TextAreaField('Remarks', [validators.Optional()])


