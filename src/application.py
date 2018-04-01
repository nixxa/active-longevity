# -*- coding: utf-8 -*-
"""
The flask application package.
"""
#pylint: disable=C0103
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPDigestAuth
from flask_wtf.csrf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension

from config import DevelopmentConfig, ProductionConfig


mode = os.environ.get('APP_MODE', 'DEBUG')

app = Flask(__name__)
if mode == 'DEBUG':
    app.config.from_object(DevelopmentConfig())
else:
    app.config.from_object(ProductionConfig())

db = SQLAlchemy(app)
auth = HTTPDigestAuth()
csrf = CSRFProtect(app)
if app.debug:
    toolbar = DebugToolbarExtension(app)

users = {
    "admin": "123Qwe",
    "user": "user"
}


@auth.get_password
def get_pw(username):
    """
    Password validation
    """
    if username in users:
        return users.get(username)
    return None


@app.context_processor
def inject_debug():
    """
    Inject DEBUG variable to all templates
    """
    return dict(debug=app.debug)


import views #pylint: disable=C0413,W0611
