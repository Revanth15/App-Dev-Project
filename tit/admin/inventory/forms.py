from wtforms import StringField, SelectField, IntegerField, TextAreaField, FileField, validators, PasswordField
import wtforms
from wtforms.fields import EmailField, DateField
from wtforms.widgets.core import NumberInput
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError
import datetime

def validate_card(form, field):
    card_number = field.data
    temp = str(card_number)

    sum_1 = 0
    sum_2 = 0

    index = len(temp) - 1

    while index >= 0:
        sum_1 += int(temp[index])
        index -= 2

    index = len(temp) - 2
    while index >= 0:
        number = int(temp[index]) * 2
        if number >= 10:
            number = str(number)
            sum_2 += int(number[0]) + int(number[1])
        else:
            sum_2 += number
        index -= 2

    sum_of_total = str(sum_2 + sum_1)
    validation = int(sum_of_total[len(sum_of_total) - 1])

    if validation != 0:
        raise ValidationError('Card number is Invalid')

def validatecvv(form, field):
    if len(field.data) > 4 or len(field.data) < 3:
        raise ValidationError('Enter the 3 or 4 digit number that is found at the back of the credit/debit card')


class CreateProductForm(FlaskForm):
    product_name = StringField('Product Name', [validators.length(min=1, max=100), validators.data_required()])
    sku = StringField('SKU', [validators.length(min=8, max=12), validators.data_required()]) #SKU = Stock Keeping Unit
    product_price = IntegerField('Product Price', [validators.NumberRange(min=1, max=10000), validators.data_required()], widget=NumberInput())
    quantity = IntegerField('Quantity', [validators.NumberRange(min=1, max=10000), validators.data_required()], widget=NumberInput())
    product_description = TextAreaField('Product Description', [validators.length(min=0, max=250), validators.data_required()])
    file = FileField('Product Photo', [validators.data_required()])
    category = SelectField('Category', [validators.data_required()], choices=[('T-Shirts & Tops','T-Shirts & Tops'),('Jeans & Joggers','Jeans & Joggers'),('Shorts & Skirts','Shorts & Skirts'),('Dresses','Dresses'),('Hoodies','Hoodies')], coerce=str)

class Checkout(FlaskForm):
    name = StringField('Name', [validators.length(min=1), validators.data_required()])
    address = StringField('Address', [validators.data_required()])
    unit_number = StringField('Unit Number', [validators.data_required()])
    postal_code = StringField('Postal Code', [validators.data_required()])
    email = EmailField('Email', [validators.data_required()])
    phone_number = IntegerField('Phone Number', [validators.data_required()])
    card_number = StringField('Card Number', [validators.length(min=13, max=16), validators.data_required(),validate_card])
    card_holder = StringField('Card Holder Name', [validators.data_required()])
    exp_mm = SelectField('Expiration MM', choices = [('1', '1'),('2', '2'),('3', '3'),('4', '4'),('5', '5'),('6', '6'),('7', '7'),('8', '8'),('9', '9'),('10', '10'),('11', '11'),('12', '12')], coerce=str)
    exp_yy = SelectField('Expiration YY', choices = [('2022','2022'),('2023','2023'),('2024','2024'),('2025','2025'),('2026','2026'),('2027','2027'),('2028','2028'),('2029','2029'),('2030','2030'),('2031','2031'),('2032','2032')], coerce=str)
    cvv = PasswordField('CVV',  [validators.data_required(),validatecvv])


class RestockForm(FlaskForm): 
    sku_select = wtforms.SelectField('SKU', choices = [], coerce=str)
    delivery_date = DateField('Delivery Date', [validators.data_required()])
    restock_quantity = IntegerField('Restock Quantity', [validators.NumberRange(min=1, max=10000), validators.data_required()], widget=NumberInput())

class ImportForm(FlaskForm):
    xlsx = FileField('Import Excel File', [validators.data_required()])

    
