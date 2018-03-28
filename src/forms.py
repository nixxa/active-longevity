from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FileField


class ChecklistForm(FlaskForm):
    executor = StringField()
    activity = StringField()
    county = StringField()
    district = StringField()
    day = IntegerField()
    month = IntegerField()
    year = IntegerField()
    visitors = IntegerField()
    photo = FileField()
