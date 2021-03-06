from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, DateField, FileField
from wtforms.validators import DataRequired, Length


class SearchForm(FlaskForm):
    search_type = StringField("Search Type", validators=[DataRequired()])
    query = StringField("Query")
    img = FileField("Image")
    types = SelectMultipleField("Types")
    locations = SelectMultipleField("Locations")
    start_date = DateField("Start Date")
    end_date = DateField("End Date")
    submit = SubmitField("Submit")
