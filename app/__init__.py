from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.pages import home, problemSet, problem

def createApp() -> Flask:
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.register_blueprint(home)
    app.register_blueprint(problemSet)
    app.register_blueprint(problem)
    db.create_all()
    return app

app = createApp()
db = SQLAlchemy(app)