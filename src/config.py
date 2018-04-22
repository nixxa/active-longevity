# -*- coding: utf-8 -*-
"""
Configuration module
"""
import os


class Config(object):
    """
    Configuration base, for all environments.
    """
    DEBUG = False
    TESTING = False
    HOSTNAME = 'check-service.ru'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@localhost:5432/longevity'.format(
        os.environ.get('DB_USER', 'longevity'),
        os.environ.get('DB_PASS', '123Qwe'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "whqw457891dnqqwr1"
    CSRF_ENABLED = True
    LOGGER_HANDLER_POLICY = 'always'
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', '')
    SESSION_TYPE = 'sqlalchemy'
    DEFAULT_USER = os.environ.get('DEF_USER', 'user')
    DEFAULT_PASS = os.environ.get('DEF_PASS', 'user')
    DEFAULT_ROLE = os.environ.get('DEF_ROLE', 'admin')


class ProductionConfig(Config):
    """
    production configuration
    """
    DEBUG = False
    SECRET_KEY = "hwd02328ncs.wrk4"


class DevelopmentConfig(Config):
    """
    Development configuration
    """
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    HOSTNAME = 'localhost:5000'
    DEBUG_TB_PROFILER_ENABLED = True


class TestingConfig(Config):
    """
    Test configuration
    """
    TESTING = True
