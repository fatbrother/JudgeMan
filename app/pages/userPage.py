from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..database import accounts

user = Blueprint('user', __name__)

@user.route('/user/<username>')
@login_required
def index(username):
    id = current_user.get_id()
    userInfo = accounts.searchById(id=id)
    return render_template('user.html', userInfo=userInfo)