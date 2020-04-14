from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class UpdatePwdForm(FlaskForm):
    password = PasswordField("New Password", validators=[DataRequired(), Length(min=5, max=20)])
    confirmPassword = PasswordField("Confirm New Password",
                                    validators=[DataRequired(), Length(min=5, max=20), EqualTo('password')])
    submit = SubmitField("Submit")
