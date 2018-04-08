# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FileField, DateField, SelectField


class ChecklistForm(FlaskForm):
    executor = StringField()
    activity = StringField()
    county = StringField()
    district = StringField()
    date = DateField()
    visitors = IntegerField()
    photo = FileField()


class FilterReportsForm(FlaskForm):
    category = SelectField('category', coerce=str)
    name = SelectField()
    district = SelectField()
    executor = SelectField()
