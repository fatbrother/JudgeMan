from flask import Blueprint, render_template
from app import db

problem = Blueprint('problem', __name__)

@problem.route('/problem/<int:problemId>')
def index(problemId):
    problem = db.session.query(db.models.Problems).filter_by(id=problemId).first()
    return render_template('problem.html', problem=problem)