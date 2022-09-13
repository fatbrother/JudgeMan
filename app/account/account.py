from flask import url_for, redirect
from flask_login import UserMixin
import json
from app import db, login_manager, bcrypt

class User(UserMixin):
    def __init__(self, userImfo: dict):
        self.id = userImfo['id']
        self.email = userImfo['email']
        self.username = userImfo['username']
        self.level = userImfo['level']
        self.passProblems = json.loads(userImfo['passProblems'])

@login_manager.user_loader
def user_loader(email):
    userInfo = db.session.query(db.models.User).filter_by(email=email).first()
    if not userInfo:
        return None
    
    user = User(userInfo)

    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in db.models.User:
        return None

    user = User(db.session.query(db.models.User).filter_by(email=email).first())

    inputPassword = request.form.get('password')
    user.is_authenticated = bcrypt.check_password_hash(db.models.User[email].password, inputPassword)

    return user
    
@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))