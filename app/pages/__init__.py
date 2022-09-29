from flask import Flask
from .homePage import home
from .problemPage import problem
from .loginPage import account
from .userPage import user
from .administratorPage import administrator

def registerBlueprints(app: Flask) -> None:
    app.register_blueprint(home)
    app.register_blueprint(problem)
    app.register_blueprint(account)
    app.register_blueprint(user)
    app.register_blueprint(administrator)