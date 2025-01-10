from datetime import timedelta
import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "..", "webapp.db")

SECRET_KEY = "khioHYG^&*HVbiuopph*GHUI976g"

REMEMBER_COOKIE_DURATION = timedelta(days=5)

SQLALCHEMY_TRACK_MODIFICATIONS = False
