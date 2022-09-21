from flask import request, render_template, redirect, Blueprint, session
from flask_login import login_user, logout_user
from app import bcrypt
from ..account.account import User
from ..database import accounts

account = Blueprint('account', __name__)


@account.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
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

        user = User(id=userInfo.id, email=userInfo.email, username=userInfo.username,
                    level=userInfo.level, passProblems=userInfo.passProblems)
        login_user(user)        

        if session['lastPage'] != None:
            return redirect(session['lastPage'])
            
        return redirect('homePage.index')

    return render_template("login.html")


@account.route('/logout')
def logout():
    logout_user()
    if session['lastPage'] != None:
        return redirect(session['lastPage'])
            
    return redirect('homePage.index')


@account.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        level = 'User'
        passProblems = []

        if not email:
            error = '請輸入電子郵件'
            return render_template('register.html', error=error)

        if not username:
            error = '請輸入使用者名稱'
            return render_template('register.html', error=error)

        if not password:
            error = '請輸入密碼'
            return render_template('register.html', error=error)

        if not confirmPassword:
            error = '請再次輸入密碼'
            return render_template('register.html', error=error)

        if password != confirmPassword:
            error = '密碼不相符'
            return render_template('register.html', error=error)

        if accounts.searchByEmail(email):
            error = '電子郵件已被註冊'
            return render_template('register.html', error=error)

        if accounts.searchByUsername(username):
            error = '使用者名稱已被註冊'
            return render_template('register.html', error=error)

        accounts.insert(email=email, password=password,
                        username=username, level=level, problems=passProblems)

        userInfo = accounts.searchByEmail(email)
        user = User(id=userInfo.id, email=userInfo.email,
                    username=userInfo.username, level=userInfo.level, passProblems=userInfo.passProblems)
        login_user(user)

        if session['lastPage'] != None:
            return redirect(session['lastPage'])
            
        return redirect('homePage.index')

    return render_template("register.html")
