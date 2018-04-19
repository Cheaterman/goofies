from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.update({
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,

    # User config below
    'SITE_NAME': 'Goofies',
    'SITE_DESCRIPTION': 'help people buy your stuff!',
    'SUPPORT_EMAIL': 'support@goofies.local',
    'PAYPAL_MODE': 'sandbox',
    'PAYPAL_CLIENT_ID': 'YOUR CLIENT ID',
    'PAYPAL_CLIENT_SECRET': 'YOUR CLIENT SECRET',
    'EMAIL_HOST': 'YOUR HOST',
    'EMAIL_HOST_USER': 'YOUR @ USER.COM',
    'EMAIL_HOST_PASSWORD': 'YOUR PASSWORD',
    'EMAIL_PORT': 587,
    'EMAIL_TLS': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///goofies.db',
})
app.secret_key = 'YOUR SECRET KEY'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from . import views  # noqa
