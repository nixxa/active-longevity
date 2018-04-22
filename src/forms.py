# -*- coding: utf-8 -*-
"""
Application forms
"""
from flask import redirect, url_for
from flask_wtf import FlaskForm
from wtforms.validators import Required, Length, EqualTo, Email
from wtforms import (
    StringField, IntegerField, FileField, DateField, SelectField, HiddenField, PasswordField)
from wtforms.fields.html5 import EmailField
from functions import is_safe_url, get_redirect_target


class RedirectForm(FlaskForm):
    """
    Base form with redirect
    """
    next = HiddenField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self, endpoint='home_action', **values):
        """
        Redirect to right place
        """
        if is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))


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
    email = EmailField('E-mail', validators=[
        Required('Поле обязательно для заполнения'),
        Length(min=3, max=100, message='Размер строки должен быть от 3 до 100 символов'),
        Email('Некорректный e-mail')])
    fullname = StringField('Полное имя', validators=[
        Length(min=3, max=100, message='Размер строки должен быть от 3 до 100 символов')])
    password = PasswordField('Пароль', validators=[
        Required('Поле обязательно для заполнения'),
        Length(min=6, max=10, message='Пароль должен быть от 6 до 10 символов'),
        EqualTo('confirm', message='Пароли должны совпадать')])
    confirm = PasswordField('Пароль еще раз')


class RegisterConfirmForm(FlaskForm):
    """
    Registration confirmation
    """
    code = StringField(
        'Введите код подтверждения, высланный на вашу электронную почту', 
        validators=[
            Required('Поле обязательно для заполнения'),
            Length(min=6, max=6, message='Неправильно заполнено поле')])


class LoginForm(RedirectForm):
    """
    Login form
    """
    username = StringField('E-mail', validators=[
        Required('Поле обязательно для заполнения'),
        Length(min=3, max=100)])
    password = PasswordField('Пароль', validators=[
        Required('Поле обязательно для заполнения')])


class RecoverPasswordForm(FlaskForm):
    """
    Recover password form
    """
    email = EmailField('E-mail', validators=[
        Required('Поле обязательно для заполнения'),
        Length(min=3, max=100, message='Размер строки должен быть от 3 до 100 символов'),
        Email('Некорректный e-mail')
    ])


class RecoverPasswordFormPhase2(FlaskForm):
    """
    Recover password form - setting new password
    """
    guid = HiddenField()
    password = PasswordField('Пароль', validators=[
        Required('Поле обязательно для заполнения'),
        Length(min=6, max=10, message='Пароль должен быть от 6 до 10 символов'),
        EqualTo('confirm', message='Пароли должны совпадать')])
    confirm = PasswordField('Пароль еще раз')
