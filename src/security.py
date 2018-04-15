#coding: utf-8
"""
Authentication rules and functions
"""
import functools
import hashlib

from flask import Response, request, session
from sqlalchemy.orm.exc import NoResultFound

from application import config
from models import User


class UserStub:
    role = 'admin'


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
    return Response(
        str('Требуется авторизация').encode('utf-8'),
        401,
        {'WWW-Authenticate': str('Basic realm="Московское долголетие"').encode('utf-8')}
    )


def user_in_role(username, roles):
    if session['user']:
        return session['user'].role in roles
    try:
        user = User.query.filter_by(email=username).one()
    except NoResultFound:
        return False
    return user.role in roles


def authorize(role_name):
    """ Auth decorator """
    def auth_decorated(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            """ Decorate request """
            auth = request.authorization
            if not auth or not check_auth(auth.username, auth.password) \
                or not user_in_role(auth.username, role_name):
                return authenticate()
            return func(*args, **kwargs)
        return decorated
    return auth_decorated
