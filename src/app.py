"""
The flask application package.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPDigestAuth
from flask_wtf.csrf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

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
    if username in users:
        return users.get(username)
    return None

import views
