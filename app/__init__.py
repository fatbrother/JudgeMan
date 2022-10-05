from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user


def createApp() -> tuple[Flask, SQLAlchemy, Bcrypt, LoginManager]:
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'fatbrother0422issohandsome'
    db = SQLAlchemy(app)
    bcrypt = Bcrypt(app)
    login_manager = LoginManager(app)
    login_manager.session_protection = "strong"
    login_manager.login_view = 'login'

    return app, db, login_manager, bcrypt

app, db, login_manager, bcrypt = createApp()
from .pages import registerBlueprints
registerBlueprints(app)