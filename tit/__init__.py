from flask import Flask
from flask_recaptcha import ReCaptcha

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kiss my ass'
app.config['UPLOAD_EXTENSIONS'] = ['jpg', 'png', 'gif', 'jfif']
app.config['RECAPTCHA_SITE_KEY'] = '6LeYegseAAAAAOeKtlVf4JudriAYmNNpp8fWNG2M'
app.config['RECAPTCHA_SECRET_KEY'] = '6LeYegseAAAAABZDV1arEbhPHpsdIjN2-W1buxNV'
recaptcha = ReCaptcha(app)

from tit.admin.routes import admin
from tit.main.routes import main

app.register_blueprint(admin)
app.register_blueprint(main)

