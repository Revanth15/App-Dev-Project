from wtforms import Form, StringField, TextAreaField, IntegerField, FileField, validators, SelectField, PasswordField
# from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf import FlaskForm
from wtforms.fields.datetime import DateField

class editVouchersForm(FlaskForm):
    vname = StringField('Voucher Name', [validators.Length(min=1, max=80), validators.DataRequired()])
    vdescription = TextAreaField('Voucher Description', [validators.DataRequired()])
    vcode = StringField('Discount Code', [validators.Length(min=8, max=8), validators.DataRequired()])
    spools_needed = StringField('Spools Needed', [validators.Length(min=-0, max=4), validators.InputRequired()])
    vamount = IntegerField('Discount Amount (%)', [validators.NumberRange(min=1, max=100), validators.DataRequired()])
    vexpirydate = DateField('Expiry Date', format='%Y-%m-%d')
    vquantity = IntegerField('Quantity ', [validators.NumberRange(min=1, max=1000), validators.DataRequired()])
    file = FileField('Voucher Picture', [validators.data_required()])


class addVouchersForm(FlaskForm):
    vname = StringField('Voucher Name', [validators.Length(min=1, max=80), validators.DataRequired()])
    vdescription = TextAreaField('Voucher Description', [validators.DataRequired()])
    vcode = StringField('Discount Code', [validators.Length(min=8, max=8), validators.DataRequired()])
    spools_needed = StringField('Spools Needed', [validators.Length(min=-0, max=4), validators.InputRequired()])    
    vamount = IntegerField('Discount Amount (%)', [validators.NumberRange(min=1, max=100), validators.DataRequired()])
    vexpirydate = DateField('Expiry Date', format='%Y-%m-%d')
    vquantity = IntegerField('Quantity ', [validators.NumberRange(min=1, max=1000), validators.DataRequired()])
    file = FileField('Voucher Picture', [validators.data_required()])