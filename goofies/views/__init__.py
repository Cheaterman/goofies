from .. import app, db
from ..forms import LoginForm, RegisterForm
from ..model import User
from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_emails import Message
from functools import wraps
from urlparse import urlparse, urljoin
import uuid


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        data = form.data
        for key in dict(data):
            if key not in dir(User):
                del data[key]

        data['activation_key'] = uuid.uuid4().hex

        user = User(**data)

        db.session.add(user)
        db.session.commit()

        message = Message(
            html=render_template('activation_email.html', user=user),
            subject='Activate your account - {}'.format(
                app.config['SITE_NAME']
            ),
            mail_from=(
                app.config['SITE_NAME'],
                'noreply@%s' % app.config['SUPPORT_EMAIL'].split('@')[1],
            ),
        )
        response = message.send(to=(
            '{} {}'.format(user.first_name, user.last_name),
            user.email,
        ))

        flash(
            'Your account was successfully created{}.'.format(
                '' if response.status_code == 250 else (
                    ', but your activation e-mail could not be sent. '
                    'Contact us at {} in order to activate your account.'
                ).format(app.config['SUPPORT_EMAIL'])
            )
        )
        return redirect(url_for('index'))

    return render_template('register.html', form=form)


@app.route('/activate/<key>')
def activate(key):
    user = User.query.filter_by(activation_key=key).first()

    if not user:
        abort(404)

    if user.active:
        flash('Your account is already active!')
        return redirect(url_for('index'))

    user.active = True
    db.session.commit()

    flash('Your account was successfully activated!')
    return redirect(url_for('index'))


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data,
            password=User.password_hash(form.password.data),
        ).first()

        if not user:
            flash('Invalid e-mail address or password!')
        else:
            login_user(user)
            if user.active:
                flash('You are now logged in.')
            else:
                flash('You must activate your account before logging in.')
            return form.redirect('index')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are now logged out.')
    return redirect(url_for('index'))


def admin_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if not current_user.admin:
            abort(403)
        return func(*args, **kwargs)
    return login_required(decorated)


from . import item, paypal, user  # noqa
