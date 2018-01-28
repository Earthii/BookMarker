"""
App configuration involving imports and such
"""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# this is needed for sessions and flashes. Key objected from urandom
app.config['SECRET_KEY'] = "b'L\x10\xd3X4\xcaF\xa1\xcb\xb1H\xa7\xbfu\xe4\xdf*nO\xc1\x0ca\x07H'"
# db, sqlite is bundled with python, no installation
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['DEBUG'] = True
db = SQLAlchemy(app)

# setting up loging feature
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"  # if not logged in, will redirect to that page
login_manager.init_app(app)

# these imports need to be here since they depend on app and db
from app import models
from app import views