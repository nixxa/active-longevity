# -*- coding: utf-8 -*-
"""
The flask application package.
"""
#pylint: disable=C0103
import os
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPDigestAuth
from flask_wtf.csrf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension

from config import DevelopmentConfig, ProductionConfig
from jinja_extentions import register_extentions

def configure_log_handler(app_mode):
    """
    Configure application logging
    """
    handler = logging.StreamHandler()
    if app_mode != 'DEBUG':
        # create file time rotating handler
        handler = TimedRotatingFileHandler(
            filename=os.environ.get('APP_LOG_FILENAME', 'app.log'),
            when='D',
            backupCount=5,
            encoding='UTF-8'
        )
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(
        fmt='%(asctime)s %(name)-10s %(levelname)-7s %(message)s',
        datefmt='%H:%M:%S'))
    # get root logger
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return handler

mode = os.environ.get('APP_MODE', 'DEBUG')

app = Flask(__name__)
log_handler = configure_log_handler(mode)
del app.logger.handlers[:]
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.DEBUG)

app.logger.info('Starting application in %s mode', mode)
if mode == 'DEBUG':
    app.config.from_object(DevelopmentConfig())
else:
    app.config.from_object(ProductionConfig())

# register jinja2 extentions
register_extentions(app)
# register database
db = SQLAlchemy(app)
# register auth
auth = HTTPDigestAuth()
# register CSRF
csrf = CSRFProtect(app)
# regionster debug toolbar
if app.debug:
    toolbar = DebugToolbarExtension(app)

# users list
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


@app.teardown_request       
def teardown_request(exception):
    """
    Autocommit session on request teardown
    """
    if exception:
        app.logger.error(exception)
    try:
        db.session.commit()
    except Exception as e:
        app.logger.error(e)
        db.session.rollback()
    finally:
        db.session.close()
        db.session.remove()


import views #pylint: disable=C0413,W0611
