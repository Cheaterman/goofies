from hashlib import sha256
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from .. import db, login_manager


@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))


class User(db.Model):
    id = Column(Integer, primary_key=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    company = Column(String(128))
    password = Column(String(64), nullable=False)
    active = Column(Boolean, server_default='0', nullable=False)
    activation_key = Column(String(64), nullable=False)
    admin = Column(Boolean, server_default='0', nullable=False)

    orders = relationship('Order', back_populates='buyer')

    def __setattr__(self, attr, value):
        if attr == 'password':
            value = self.password_hash(value)
        super(User, self).__setattr__(attr, value)

    def __repr__(self):
        return ('User('
            'id={id!r}, '
            'first_name={first_name!r}, '
            'last_name={last_name!r}, '
            'email={email!r}, '
            'company={company!r}, '
            'active={active!r}, '
            'activation_key={activation_key!r}, '
            'admin={admin!r}'
        ')'.format(**self.__dict__))

    @property
    def paid_orders(self):
        return len([order for order in self.orders if order.paid])

    @staticmethod
    def password_hash(password):
        return sha256(password.encode('utf8')).hexdigest()

    is_authenticated = True
    is_anonymous = False

    @property
    def is_active(self):
        return self.active

    def get_id(self):
        return str(self.id)
