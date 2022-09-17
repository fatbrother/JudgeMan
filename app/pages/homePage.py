from flask import Blueprint, render_template
from app.database.models import ProblemSet

home = Blueprint('home', __name__)

@home.route('/')
def index():
    problemSets = ProblemSet.query.all()
    return render_template('home.html', problemSets=problemSets)

@home.route('/<string:problemSetName>')
def problemSetPage(problemSetName):
    problemSet = ProblemSet.query.filter_by(name=problemSetName).first()
    return render_template('problemSet.html', problemSet=problemSet)