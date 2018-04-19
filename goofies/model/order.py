from sqlalchemy import (
    Boolean,
    Column,
    Numeric,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from .. import db


class Order(db.Model):
    id = Column(Integer, primary_key=True)
    buyer_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
    amount = Column(Numeric, nullable=False)
    payment_id = Column(String(128))
    paid = Column(Boolean, server_default='0', nullable=False)

    buyer = relationship('User', back_populates='orders')
    item = relationship('Item')

    def __repr__(self):
        return ('Order('
            'id={id!r}, '
            'buyer={buyer!r}, '
            'item={item!r}, '
            'amount={amount!r}, '
            'payment_id={payment_id!r}, '
            'paid={paid!r}'
        ')'.format(**self.__dict__))
