from flask import request, render_template, url_for, redirect, flash, Blueprint
from flask_login import login_user, logout_user, current_user
from app import db, bcrypt
from app.account.account import User

login = Blueprint('login', __name__)

@login.route('/login', methods=['GET', 'POST'])
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

    userInfo = db.session.query(db.models.User).filter_by(email=email).first()

    if not userInfo:
        flash('Email not found')
        return redirect(url_for('login'))
    
    if not bcrypt.check_password_hash(userInfo.password, password):
        flash('Password incorrect')
        return redirect(url_for('login'))

    user = User(userInfo)
    login_user(user)

    return redirect(url_for('home'), current_user=current_user)

@login.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@login.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    confirmPassword = request.form['confirmPassword']

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
    
    if db.session.query(db.models.User).filter_by(email=email).first():
        flash('Email already exists')
        return redirect(url_for('register'))
    
    if db.session.query(db.models.User).filter_by(username=username).first():
        flash('Username already exists')
        return redirect(url_for('register'))
    
    userInfo = db.models.User(email=email, username=username, password=bcrypt.generate_password_hash(password).decode('utf-8'), level='User', passProblems='[]')
    db.session.add(userInfo)
    db.session.commit()

    user = User(userInfo)
    login_user(user)

    return redirect(url_for('home'), current_user=current_user)
