from flask import Flask, request
from flask_recaptcha import ReCaptcha

app = Flask(__name__)
app.config.from_object('config')
recaptcha = ReCaptcha(app)


from tit.admin.routes import admin
from tit.main.routes import main

app.register_blueprint(admin)
app.register_blueprint(main)

