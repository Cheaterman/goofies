import paypalrestsdk
from . import app

paypalrestsdk.configure(dict(
    mode=app.config['PAYPAL_MODE'],
    client_id=app.config['PAYPAL_CLIENT_ID'],
    client_secret=app.config['PAYPAL_CLIENT_SECRET'],
))
