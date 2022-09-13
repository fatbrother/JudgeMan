from flask import Blueprint, render_template, request
from account import accountManager

user = Blueprint('user', __name__)

@user.route('/user/<username>')
def index(username):
    userImfo = accountManager.getAccount(username)
    return render_template('user.html', userImfo=userImfo)