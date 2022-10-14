from flask import Blueprint, redirect, url_for, session, render_template, request
from flask_login import login_required, current_user
from ..database import accounts

administrator = Blueprint('administrator', __name__)

@administrator.route('/administrator', methods=['GET', 'POST'])
@login_required
def administratorPage():
    user = accounts.searchById(current_user.id)
    if not user.level == 'Administrator':
        return redirect(session['lastPage'])

    if request.method == 'POST':
        if 'accept' in request.form:
            accounts.update(int(request.form['id']), level='User')
        elif 'reject' in request.form:
            accounts.delete(int(request.form['id']))
        elif 'updateLevel' in request.form:
            accounts.update(int(request.form['id']), level=request.form['level'])

    session['lastPage'] = url_for('administrator.administratorPage')

    allUser = accounts.viewAll()
    waitingList = []
    for user in allUser:
        if user.level == 'Waiting':
            waitingList.append(user)

    return render_template('administrator.html', waitingList=waitingList, allUser=allUser)

    