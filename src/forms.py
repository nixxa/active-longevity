# -*- coding: utf-8 -*-
"""
Application forms
"""
from flask import redirect, url_for
from flask_wtf import FlaskForm
from wtforms.validators import Required, Length, EqualTo
from wtforms import (
    StringField, IntegerField, FileField, DateField, SelectField, HiddenField, PasswordField)
from functions import is_safe_url, get_redirect_target


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
    email = StringField('E-mail', validators=[Required(), Length(min=3, max=100)])
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


class RedirectForm(FlaskForm):
    next = HiddenField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self, endpoint='home_action', **values):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))


class LoginForm(RedirectForm):
    """
    Login form
    """
    username = StringField('E-mail', validators=[Required('Поле обязательно для заполнения'), Length(min=3, max=100)])
    password = PasswordField('Пароль', validators=[Required('Поле обязательно для заполнения')])
