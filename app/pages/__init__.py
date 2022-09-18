from flask import Flask
from .homePage import home
from .problemPage import problem
from .loginPage import account
from .testPage import test
from .userPage import user

def registerBlueprints(app: Flask) -> None:
    app.register_blueprint(home)
    app.register_blueprint(problem)
    app.register_blueprint(account)
    app.register_blueprint(test)
    app.register_blueprint(user)