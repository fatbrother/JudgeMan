from flask import Blueprint, render_template
from app import db


problemSet = Blueprint('problemSet', __name__)

@problemSet.route('/problemSet')
def index():
    problemSet = db.problemSet.allView()
    return render_template('problemSet.html', problemSet=problemSet)