from .. import db
from sqlalchemy import Column, Integer, Numeric, String


class Item(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    price = Column(Numeric, nullable=False)
    quantity = Column(Integer, nullable=False)

    def __repr__(self):
        return ('Item('
            'id={id!r}, '
            'name={name!r}, '
            'price={price!r}, '
            'quantity={quantity!r}'
        ')'.format(**self.__dict__))
