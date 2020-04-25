from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.dbModels.users import Users
from application import db
from wtforms.fields.core import RadioField
from application.forms.RegisterForm import RegisterForm

class NewUserForm(RegisterForm):
    isAdmin = BooleanField("Is Admin?")