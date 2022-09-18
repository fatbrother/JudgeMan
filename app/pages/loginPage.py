from distutils.log import error
from flask import request, render_template, url_for, redirect, flash, Blueprint
from flask_login import login_user, logout_user, current_user
from app import bcrypt
from ..account.account import User
from ..database import accounts

account = Blueprint('account', __name__)


@account.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    email = request.form['email']
    password = request.form['password']

    if not email:
        error = "請輸入電子郵件"
        return render_template("login.html", error=error)

    if not password:
        error = "請輸入密碼"
        return render_template("login.html", error=error)

    userInfo = accounts.searchByEmail(email)

    if not userInfo:
        error = "電子郵件或密碼錯誤"
        return render_template("login.html", error=error)

    if not bcrypt.check_password_hash(userInfo.password, password):
        error = "電子郵件或密碼錯誤"
        return render_template("login.html", error=error)

    user = User(userInfo)
    login_user(user)

    return redirect(url_for('home'), current_user=current_user)


@account.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@account.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")

    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    confirmPassword = request.form['confirmPassword']
    level = 'User'
    passProblems = []

    if not email:
        error = 'Please enter your email address'
        return redirect(url_for('account.register', error=error))

    if not username:
        error = 'Please enter your username'
        return redirect(url_for('account.register', error=error))

    if not password:
        flash('Please enter your password')
        return redirect(url_for('account.register'))

    if not confirmPassword:
        flash('Please confirm your password')
        return redirect(url_for('account.register'))

    if password != confirmPassword:
        flash('Password and confirm password do not match')
        return redirect(url_for('account.register'))

    if accounts.searchByEmail(email):
        flash('Email already exists')
        return redirect(url_for('account.register'))

    if accounts.searchByUsername(username):
        flash('Username already exists')
        return redirect(url_for('account.register'))

    accounts.update(email=email, password=password,
                    username=username, level=level, passProblems=passProblems)

    userInfo = accounts.searchByEmail(email)
    user = User(id=userInfo.id, email=userInfo.email, password=userInfo.password,
                username=userInfo.username, level=userInfo.level, passProblems=userInfo.passProblems)
    login_user(user)

    return redirect(url_for('home'), current_user=current_user)
