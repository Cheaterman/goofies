from .. import app, db
from ..forms import ItemCreateForm
from ..model import Item
from . import admin_required
from flask import flash, redirect, render_template


@app.route('/shop')
def shop():
    return render_template('shop.html', items=Item.query)


@app.route('/shop/<int:id>')
def view_shop_item(id):
    item = Item.query.get_or_404(id)
    return render_template('view_shop_item.html', item=item)


@app.route('/items')
@admin_required
def items():
    return render_template('items.html', items=Item.query)


@app.route('/item/add', methods=('GET', 'POST'))
@admin_required
def add_item():
    form = ItemCreateForm()

    if form.validate_on_submit():
        data = form.data
        for field in dict(data):
            if field not in dir(Item):
                del data[field]

        db.session.add(Item(**data))
        db.session.commit()

        flash('Your item was created successfully.')
        return redirect('items')

    return render_template('item_add.html', form=form)


@app.route('/item/delete/<int:id>', defaults=dict(confirm=False))
@app.route('/item/delete/<int:id>/confirm', defaults=dict(confirm=True))
@admin_required
def delete_item(id, confirm=False):
    item = Item.query.get_or_404(id)
    if confirm:
        db.session.delete(item)
        db.session.commit()

        flash('Your item was deleted successfully.')
        return redirect('items')

    return render_template('item_delete.html', item=item)
