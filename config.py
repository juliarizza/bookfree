import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "bookfree.db")
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = "chavebemdificil"
WTF_CSRF_ENABLED = True
