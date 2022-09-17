from flask import Blueprint, render_template
from app.database.models import Problem

problem = Blueprint('problem', __name__)

@problem.route('/problem/<int:problemId>')
def index(problemId):
    problem = Problem.query().filter_by(id=problemId).first()
    return render_template('problem.html', problem=problem)