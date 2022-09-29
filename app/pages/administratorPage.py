from flask import Blueprint, redirect, url_for, session, render_template, request
from flask_login import login_required, current_user
from ..database import accounts

administrator = Blueprint('administrator', __name__)

@administrator.route('/administrator', methods=['GET', 'POST'])
@login_required
def administratorPage():
    if request.method == 'POST':
        if request.form['accept']:
            accounts.update(int(request.form['id']), level='User')

    

    user = accounts.searchById(current_user.id)
    if not user.level == 'Administrator':
        return redirect(session['lastPage'])

    session['lastPage'] = url_for('administrator.administratorPage')

    allUser = accounts.viewAll()
    waitingList = []
    for user in allUser:
        if user.level == 'Waiting':
            waitingList.append(user)

    return render_template('administrator.html', waitingList=waitingList)

    