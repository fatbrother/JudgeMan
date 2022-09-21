from flask import Blueprint, render_template, url_for, session
from ..database import problemSets

home = Blueprint('home', __name__)

@home.route('/',  methods=['GET', 'POST'])
def index():
    session['lastPage'] = url_for('home.index')
    # return render_template('home.html', problemSets=problemSets.viewAll())
    return render_template('home.html', problemSets=problemSets.viewAll()[1:-1])