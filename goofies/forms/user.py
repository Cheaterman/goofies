from wtforms import BooleanField
from .register import RegisterForm, unique_email


class UserEditForm(RegisterForm):
    active = BooleanField('Active')
    admin = BooleanField('Admin')

    def __init__(self, *args, **kwargs):
        validators = self.email.kwargs['validators']
        if unique_email in validators:
            validators.remove(unique_email)
        return super(UserEditForm, self).__init__(*args, **kwargs)
