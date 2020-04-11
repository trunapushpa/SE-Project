from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.dbModels.users import Users
from application import db

class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=5, max=50)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=5, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=5, max=20)])
    confirmPassword = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=5, max=20), EqualTo('password')])
    submit = SubmitField("Submit")

    def validate_email(self, email):
        #breakpoint()
        user = db.session.query(Users).filter(Users.email == email.data).first()
        if(user):
            raise ValidationError("Email already registered, Please user another!!")

