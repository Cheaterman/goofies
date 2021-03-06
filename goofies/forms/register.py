from flask_wtf import FlaskForm
from wtforms import (
    PasswordField,
    StringField,
    SubmitField,
    ValidationError,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length
from wtforms.widgets import Input
from ..model import User


def unique_email(self, field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError(
            'An account with this e-mail address already exists!'
        )


class RegisterForm(FlaskForm):
    first_name = StringField(
        'First name',
        validators=[InputRequired(), Length(max=128)]
    )
    last_name = StringField(
        'Last name',
        validators=[InputRequired(), Length(max=128)]
    )
    phone = StringField(
        'Phone',
        validators=[Length(max=128)],
        widget=Input(input_type='tel')
    )
    email = EmailField('E-mail', validators=[
        InputRequired(),
        Length(max=128),
        Email(),
        unique_email
    ])
    confirm_email = EmailField('Confirm e-mail', validators=[
        InputRequired(),
        EqualTo('email', message='E-mails must match!')
    ])
    company = StringField('Company', validators=[Length(max=128)])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Register')
