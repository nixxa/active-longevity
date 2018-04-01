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
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@localhost:5432/longevity'.format(
        os.environ.get('DB_USER', 'longevity'),
        os.environ.get('DB_PASS', '123Qwe'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "whqw457891dnqqwr1"
    CSRF_ENABLED = True
    LOGGER_HANDLER_POLICY = 'always'


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


class TestingConfig(Config):
    """
    Test configuration
    """
    TESTING = True
