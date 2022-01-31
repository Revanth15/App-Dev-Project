from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators
from wtforms.fields import EmailField, DateField
class CreateFeedbackForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    feedback = TextAreaField('Feedback', [validators.DataRequired()])
class CreateAccountFeedback(Form):
    account_name = StringField('Account Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    feedback = TextAreaField('Feedback', [validators.DataRequired()])
