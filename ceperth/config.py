
import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://francis:xxx@localhost:5432/cepdev"
    DEBUG = True
    SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", "")

class NewConfig(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///cepdev.db"
    DEBUG = True
    SECRET_KEY = os.environ.get("CEPDEV_SECRET_KEY", "")
    MAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")
    MAIL_SERVER ='smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'kesfrance@gmail.com'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://francis:xxx@localhost:5432/cepdev"
    DEBUG = False
    SECRET_KEY = "Not secret"
    DEBUG = True
    SECRET_KEY = os.environ.get("CEPDEV_SECRET_KEY", "")
    MAIL_PASSWORD =  os.environ.get("GMAIL_PASSWORD")
    MAIL_SERVER ='smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'kesfrance@gmail.com'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

class TravisConfig(object):
    """configuration to allow connection to tavis psogres dbase"""
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost:5432/cepdevtest"
    DEBUG = False
    SECRET_KEY = "Not secret"


