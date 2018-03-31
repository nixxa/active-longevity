"""
The flask application package.
"""
#pylint: disable=C0103
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPDigestAuth
from flask_wtf.csrf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension

from config import DevelopmentConfig


app = Flask(__name__)
app.config.from_object(DevelopmentConfig())

db = SQLAlchemy(app)
auth = HTTPDigestAuth()
csrf = CSRFProtect(app)
#toolbar = DebugToolbarExtension(app)

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

import views
