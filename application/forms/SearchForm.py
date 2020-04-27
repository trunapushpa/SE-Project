from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, DateField, FileField, HiddenField
from wtforms.validators import DataRequired, Length


class SearchForm(FlaskForm):
    search_type = StringField("Search Type", validators=[DataRequired()])
    query = StringField("Query")
    img = FileField("Image")
    f_vector = HiddenField("Feature Vector")
    types = SelectMultipleField("Types")
    locations = SelectMultipleField("Locations")
    start_date = DateField("Start Date")
    end_date = DateField("End Date")
    submit = SubmitField("Submit")
