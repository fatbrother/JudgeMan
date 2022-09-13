from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import db

user = Blueprint('user', __name__)

@user.route('/user/<username>')
@login_required
def index(username):
    email = current_user.get_id()
    userInfo = db.session.query(db.models.User).filter_by(email=email).first()
    return render_template('user.html', userInfo=userInfo)