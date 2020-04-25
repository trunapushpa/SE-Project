from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField, RadioField
from wtforms.validators import DataRequired


class MarkInactiveForm(FlaskForm):
    item_id = IntegerField('Item id', validators=[DataRequired()])
    success = StringField('Success')
    email = StringField('Email')
    submit = SubmitField('Submit')
