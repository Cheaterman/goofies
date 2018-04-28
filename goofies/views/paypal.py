from flask import abort, flash, redirect, render_template, request, url_for
from flask_emails import Message
from flask_login import current_user, login_required
from paypalrestsdk import Payment
from .. import app, db
from .. import paypal  # noqa
from ..model import Item, Order


@app.route('/pay/<int:id>')
@login_required
def pay(id):
    item = Item.query.get_or_404(id)

    order = Order(
        buyer=current_user,
        item=item,
        amount=item.price,
    )
    db.session.add(order)
    db.session.commit()

    payment = Payment(dict(
        intent='sale',
        payer=dict(payment_method='paypal'),
        redirect_urls=dict(
            return_url=url_for('execute', id=order.id, _external=True),
            cancel_url=url_for('cancel', id=order.id, _external=True),
        ),
        transactions=[dict(
            item_list=dict(items=[
                dict(
                    name=item.name,
                    price=float(item.price),
                    currency='EUR',
                    quantity=1,
                ),
            ]),
            amount=dict(total=float(item.price), currency='EUR'),
            description='Thank you for your purchase!',
        )],
    ))

    if not payment.create():
        db.session.delete(order)
        db.session.commit()

        flash('An error occured while creating your payment: {}'.format(
            payment.error
        ))
        return redirect(url_for('view_shop_item', id=item.id))

    order.payment_id = payment.id
    db.session.commit()

    for link in payment.links:
        if link.rel == 'approval_url':
            return redirect(link.href)

    abort(500)


@app.route('/payment/cancel/<int:id>')
@login_required
def cancel(id):
    order = Order.query.get(id)

    if not order or order.buyer != current_user:
        flash('Your order was not found, maybe it was already cancelled?')
        return redirect(url_for('shop'))

    if order.paid:
        flash('Your order was already paid, you cannot cancel it!')
        return redirect(url_for('shop'))

    db.session.delete(order)
    db.session.commit()

    flash('Your order was cancelled successfully.')
    return redirect(url_for('shop'))


@app.route('/payment/execute/<int:id>')
@login_required
def execute(id):
    payment = Payment.find(request.args.get('paymentId'))

    order = Order.query.get(id)

    if not order or order.buyer != current_user:
        flash('Your order was not found, maybe it was already cancelled?')
        return redirect(url_for('shop'))

    if order.paid:
        flash('Your order was already paid, not charging you twice!')
        return redirect(url_for('shop'))

    if order.payment_id != payment.id:
        flash('This payment does not seem to match your order!')
        return redirect(url_for('shop'))

    if not payment.execute(dict(payer_id=request.args.get('PayerID'))):
        flash('An error occured while processing your order: {}'.format(
            payment.error
        ))
        return redirect(url_for('shop'))

    order.paid = True
    order.item.quantity -= 1
    db.session.commit()

    message = Message(
        html=render_template(
            'order_receipt.html',
            order=order,
            item=order.item,
            user=order.buyer,
        ),
        subject='Receipt for your purchase - {}'.format(
            app.config['SITE_NAME']
        ),
        mail_from=(
            app.config['SITE_NAME'],
            'noreply@%s' % app.config['SUPPORT_EMAIL'].split('@')[1],
        ),
    )
    user = order.buyer
    response = message.send(to=(
        '{} {}'.format(user.first_name, user.last_name),
        user.email,
    ))

    flash(
        'Your order was processed successfully{}. Thank you!'.format(
            '' if response.status_code == 250 else (
                ', but your purchase receipt could not be sent. '
                'Contact us at {} in order to get your receipt.'
            ).format(app.config['SUPPORT_EMAIL'])
        )
    )
    return redirect(url_for('shop'))
