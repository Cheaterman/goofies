from flask import redirect, request, url_for
from flask_login import login_user
from flask_wtf import FlaskForm
from urlparse import urlparse, urljoin
from wtforms import (
    HiddenField,
    PasswordField,
    StringField,
    SubmitField,
    ValidationError,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, InputRequired, Length


class LoginForm(FlaskForm):
    email = EmailField('E-mail', validators=[InputRequired(), Length(max=128), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Log in')
    next = HiddenField()

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self, target='index', **kwargs):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)
        next_target = get_redirect_target()
        return redirect(next_target or url_for(target, **kwargs))


def get_redirect_target():
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


def is_safe_url(target):
    host_url = urlparse(request.host_url)
    url = urlparse(urljoin(request.host_url, target))
    return (
        url.scheme in ('http', 'https') and
        host_url.netloc == url.netloc
    )
