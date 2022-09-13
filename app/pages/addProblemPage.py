from flask import Blueprint, render_template, request
from app import db

addProblem = Blueprint('addProblem', __name__)

@addProblem.route('/addProblem')
def index():
    if request.method == 'POST':
        title = request.form['title']
        taskDescription = request.form['taskDescription']
        inputFormat = request.form['inputFormat']
        outputFormat = request.form['outputFormat']
        sampleInput = request.form['sampleInput']
        sampleOutput = request.form['sampleOutput']
        testCaseNumber = request.form['testCaseNumber']
        AC = request.form['AC']
        WA = request.form['WA']
        db.Problems.insert(title, taskDescription, inputFormat, outputFormat, sampleInput, sampleOutput, testCaseNumber, AC, WA)

    return render_template('addProblem.html')