from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators
from wtforms.fields import EmailField, DateField
class CreateFeedbackForm(Form):
    Name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    type = SelectField('Type', [validators.DataRequired()], choices=[('', 'Select'), ('Accounts', 'Accounts'), ('Payment', 'Payment'),('Shipping','Shipping'),('Rewards','Rewards'),('Others', 'Others')], default='')
    feedback = TextAreaField('Feedback', [validators.DataRequired()])
    status = SelectField('Status', [validators.DataRequired()], choices=[('Pending', 'Pending'),('Closed', 'Closed')], default='Pending')
class CreateAccountFeedback(Form):
    account_name = StringField('Account Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    feedback = TextAreaField('Feedback', [validators.DataRequired()])
