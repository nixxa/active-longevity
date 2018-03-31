# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FileField


class ChecklistForm(FlaskForm):
    executor = StringField()
    activity = StringField()
    county = StringField()
    district = StringField()
    date = StringField()
    visitors = IntegerField()
    photo = FileField()
