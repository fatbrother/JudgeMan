from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

from app.pages import home, problemSet, problem

def createApp() -> Flask:
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.register_blueprint(home)
    app.register_blueprint(problemSet)
    app.register_blueprint(problem)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(('DATABASE_URL')) or 'sqlite:///' + './site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app

app = createApp()
db = SQLAlchemy(app)