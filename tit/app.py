from itertools import product
from flask import Flask, render_template, request, redirect, url_for, session
from tit.admin.inventory.forms import CreateProductForm, RestockForm, ImportForm, PaymentForm, Delivery
from flask_recaptcha import ReCaptcha
import datetime
import os
import email_validator
import shelve
import classes.product as Product
import classes.delivery as Delivery
import classes.import_file as import_file
import classes.payment as Payment
import uuid

app = Flask(__name__)

app.config['SECRET_KEY'] = 'kiss my ass'
app.config['UPLOAD_EXTENSIONS'] = ['jpg', 'png', 'gif', 'jfif']
app.config['RECAPTCHA_SITE_KEY'] = '6LeYegseAAAAAOeKtlVf4JudriAYmNNpp8fWNG2M'
app.config['RECAPTCHA_SECRET_KEY'] = '6LeYegseAAAAABZDV1arEbhPHpsdIjN2-W1buxNV'
recaptcha = ReCaptcha(app)
 # if recaptcha.verify():
 #   message=
 # else:
 #   message = "Please fill out teh Recaptcha!"



if __name__ == "__main__":
    app.run(debug=True)
