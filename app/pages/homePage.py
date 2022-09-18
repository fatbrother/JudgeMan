from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from ..database import problemSets

home = Blueprint('home', __name__)

@home.route('/',  methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['submit'] != None:
            return redirect(url_for('problem.index', problemId=request.form['submit']))

    return render_template('home.html', problemSets=problemSets.viewAll())