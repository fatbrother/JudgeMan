from flask import url_for, redirect
from flask_login import UserMixin
from app import login_manager
from app.database import accounts

class User(UserMixin):
    def __init__(self, id, email, username, level, passProblems):
        self.id = id
        self.email = email
        self.username = username
        self.level = level
        self.passProblems = passProblems

    def __repr__(self):
        return f"User('{self.id}', '{self.email}', '{self.username}', '{self.level}', '{self.passProblems}')"

@login_manager.user_loader
def load_user(user_id):
    userInfo = accounts.searchById(user_id)
    user = User(id=userInfo.id, email=userInfo.email, username=userInfo.username, level=userInfo.level, passProblems=userInfo.passProblems)
    return user
    
@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))