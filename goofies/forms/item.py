from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.fields.html5 import DecimalField
from wtforms.validators import InputRequired, Length, NumberRange


class ItemCreateForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=128)])
    price = DecimalField('Price', validators=[InputRequired(), NumberRange(min=0)])
    quantity = IntegerField('Available quantity', validators=[InputRequired(), NumberRange(min=1)])
    submit = SubmitField('Create')
