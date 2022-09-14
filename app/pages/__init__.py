from flask import Flask
from app.pages.homePage import home
from app.pages.problemPage import problem
from app.pages.loginPage import account

def registerBlueprints(app: Flask) -> None:
    app.register_blueprint(home)
    app.register_blueprint(problem)
    app.register_blueprint(account)