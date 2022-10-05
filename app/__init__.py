from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from decouple import config


def createApp() -> Flask:
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SQLALCHEMY_DATABASE_URI'] = config('SQLALCHEMY_DATABASE_URI') or 'sqlite:///./site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'fatbrother0422issohandsome'
    return app

app = createApp()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'

from .pages import registerBlueprints
registerBlueprints(app)