from flask import Flask
from app.pages.homePage import home
from app.pages.problemPage import problem
from app.pages.loginPage import account
from app.pages.testPage import test
from app.pages.loginPage import account
from app.pages.userPage import user

def registerBlueprints(app: Flask) -> None:
    app.register_blueprint(home)
    app.register_blueprint(problem)
    app.register_blueprint(account)
    app.register_blueprint(test)
    app.register_blueprint(account)
    app.register_blueprint(user)