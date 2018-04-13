# -*- coding: utf-8 -*-
"""
Application forms
"""
from flask_wtf import FlaskForm
from wtforms.validators import Required
from wtforms import (
    StringField, IntegerField, FileField, DateField, SelectField, HiddenField)


class ChecklistForm(FlaskForm):
    """
    Checklist form
    """
    executor = StringField()
    activity = StringField()
    county = StringField()
    district = StringField()
    date = DateField()
    visitors = IntegerField()
    photo = FileField()


class FilterReportsForm(FlaskForm):
    """
    Reports filter form
    """
    category = SelectField()
    name = SelectField()
    district = SelectField()
    executor = SelectField()


class FilterActivitiesForm(FlaskForm):
    """
    Activities filter form
    """
    category = SelectField()
    name = SelectField()
    district = SelectField()
    executor = SelectField()


class ActivityForm(FlaskForm):
    """
    Activity form
    """
    id = HiddenField()
    category = StringField()
    name = StringField()
    place = StringField()
    executor = StringField()
    address = StringField()
    county = StringField()
    district = StringField()
    planned_visitors = IntegerField()
