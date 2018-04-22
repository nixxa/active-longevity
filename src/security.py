#coding: utf-8
"""
Authentication rules and functions
"""
import functools
import hashlib

from flask import Response, request, session, redirect
from sqlalchemy.orm.exc import NoResultFound

from application import config
from models import User
from functions import get_redirect_target


class UserStub:
    role = 'admin'
    email = 'admin'
    roles = ['admin']


def check_auth(username, password):
    """
    Checks credentials
    """
    if username == config.DEFAULT_USER and password == config.DEFAULT_PASS:
        session['user'] = UserStub()
        return True
    try:
        user = User.query.filter_by(email=username).one()
    except NoResultFound:
        return False
    if user is not None:
        secret = config.SECRET_KEY
        pwd = hashlib.sha256('{}:{}'.format(password, secret).encode('utf-8')).hexdigest()
        if user.password_hash == pwd and not user.disabled and user.confirmed:
            session['user'] = user
            return True
    return False


def authenticate():
    """ Sends 401 response """
    # return Response(
    #     str('Требуется авторизация').encode('utf-8'),
    #     401,
    #     {'WWW-Authenticate': str('Basic realm="https://check-service.ru"').encode('utf-8')}
    # )
    target = get_redirect_target()
    return redirect('/login/?next=%s' % target)


def user_in_role(user, roles):
    """
    True if user has one of specified roles
    """
    if user:
        result = False
        for role in roles:
            result |= (role in user.roles)
        return result
    return False


def authorize(role_name):
    """ Auth decorator """
    def auth_decorated(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            """ Decorate request """
            auth = session.get('user', None)
            if auth is None or not user_in_role(auth, role_name):
                return authenticate()
            return func(*args, **kwargs)
        return decorated
    return auth_decorated
