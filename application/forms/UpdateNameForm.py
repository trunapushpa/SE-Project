from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class UpdateNameForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=1, max=50)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField("Submit")
