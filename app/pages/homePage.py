from flask import Blueprint, render_template
from app import db

home = Blueprint('home', __name__)

@home.route('/')
def index():
    problemSets = db.session.query(db.models.ProblemSet).all()
    return render_template('home.html', problemSets=problemSets)

@home.route('/<string:problemSetName>')
def problemSetPage(problemSetName):
    problemSet = db.session.query(db.models.ProblemSet).filter_by(name=problemSetName).first()
    return render_template('problemSet.html', problemSet=problemSet)