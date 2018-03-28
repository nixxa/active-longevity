class Config(object):
    """
    Configuration base, for all environments.
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../data/application.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "whqw457891dnqqwr1"
    CSRF_ENABLED = True


class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
	DEBUG = True


class TestingConfig(Config):
    TESTING = True
