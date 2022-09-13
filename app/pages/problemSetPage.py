from flask import Blueprint, render_template
from app import db

problemSet = Blueprint('problemSet', __name__)

@problemSet.route('/problemSet')
def index():
    problemSets = db.session.query(db.models.ProblemSet).all()
    return render_template('problemSet.html', problemSets=problemSets)

@problemSet.route('/problemSet/<string:problemSetName>')
def problemSetPage(problemSetName):
    problemSet = db.session.query(db.models.ProblemSet).filter_by(name=problemSetName).first()
    return render_template('problemSetPage.html', problemSet=problemSet)