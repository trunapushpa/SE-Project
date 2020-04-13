from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length


class UploadForm(Form):
    tag = SelectField('Tag')
    Location = SelectField('Location')
    caption = TextAreaField("Caption", validators=[DataRequired(), Length(min=5, max=100)])
    submit = SubmitField("Submit")
