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
        flash('Please enter your email address')
        return redirect(url_for('login'))
    
    if not password:
        flash('Please enter your password')
        return redirect(url_for('login'))

    userInfo = accounts.searchByEmail(email)

    if not userInfo:
        flash('Email not found')
        return redirect(url_for('login'))
    
    if not bcrypt.check_password_hash(userInfo.password, password):
        flash('Password incorrect')
        return redirect(url_for('login'))

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
        flash('Please enter your email address')
        return redirect(url_for('register'))
    
    if not username:
        flash('Please enter your username')
        return redirect(url_for('register'))
    
    if not password:
        flash('Please enter your password')
        return redirect(url_for('register'))
    
    if not confirmPassword:
        flash('Please confirm your password')
        return redirect(url_for('register'))
    
    if password != confirmPassword:
        flash('Password and confirm password do not match')
        return redirect(url_for('register'))
    
    if accounts.searchByEmail(email):
        flash('Email already exists')
        return redirect(url_for('register'))
    
    if accounts.searchByUsername(username):
        flash('Username already exists')
        return redirect(url_for('register'))
    
    accounts.update(email=email, password=password, username=username, level=level, passProblems=passProblems)

    userInfo = accounts.searchByEmail(email)
    user = User(id=userInfo.id, email=userInfo.email, password=userInfo.password, username=userInfo.username, level=userInfo.level, passProblems=userInfo.passProblems)
    login_user(user)

    return redirect(url_for('home'), current_user=current_user)
