# -*- coding: utf-8 -*-
"""
Application forms
"""
from flask_wtf import FlaskForm
from wtforms.validators import Required, Length, EqualTo
from wtforms import (
    StringField, IntegerField, FileField, DateField, SelectField, HiddenField, PasswordField)


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


class RegisterUserForm(FlaskForm):
    """
    New user registration form
    """
    email = StringField('Email', validators=[Required(), Length(min=3, max=100)])
    fullname = StringField('Полное имя', validators=[Length(max=100)])
    password = PasswordField('Пароль', validators=[
        Required(),
        Length(min=6, max=10),
        EqualTo('confirm', message='Пароли должны совпадать')])
    confirm = PasswordField('Пароль еще раз')


class RegisterConfirmForm(FlaskForm):
    """
    Registration confirmation
    """
    code = StringField('Код подтверждения', validators=[Required(), Length(min=6, max=6)])
