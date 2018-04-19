from .. import app, db
from ..forms import UserEditForm
from ..model import User
from . import admin_required
from flask import flash, redirect, render_template, url_for


@app.route('/users')
@admin_required
def users():
    return render_template('users.html', users=User.query)


@app.route('/user/<int:id>/edit', methods=('GET', 'POST'))
def edit_user(id):
    user = User.query.get_or_404(id)
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        data = form.data
        for key in dict(data):
            if key not in dir(user):
                del data[key]

        for key, value in data.items():
            setattr(user, key, value)

        flash('User {} {} was edited successfully.'.format(
            user.first_name,
            user.last_name,
        ))
        db.session.commit()

    return render_template('user_edit.html', form=form)


@app.route('/user/<int:id>/delete', defaults=dict(confirm=False))
@app.route('/user/<int:id>/delete/confirm', defaults=dict(confirm=True))
def delete_user(id, confirm=False):
    user = User.query.get_or_404(id)
    if confirm:
        db.session.delete(user)
        db.session.commit()

        flash('This user was deleted successfully.')
        return redirect(url_for('users'))

    return render_template('user_delete.html', user=user)
