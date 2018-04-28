from wtforms import BooleanField, PasswordField
from .purchase import PurchaseForm, unique_email


class UserEditForm(RegisterForm):
    password = PasswordField('Password')
    active = BooleanField('Active')
    admin = BooleanField('Admin')

    def __init__(self, *args, **kwargs):
        validators = self.email.kwargs['validators']
        if unique_email in validators:
            validators.remove(unique_email)

        super(UserEditForm, self).__init__(*args, **kwargs)

        del self.confirm_email
        self.submit.label.text = 'Submit'
