from flask import Blueprint, redirect, flash, url_for, render_template, request
from flask_login import current_user, login_required
from application import db, app
from application.dbModels.users import Users

all_users = Blueprint('all_users', __name__)

@all_users.route('/allusers', methods=['POST', 'GET'])
def allusers():
    if current_user.isadmin:
        # Logged in user should not be able to edit his/her account
        users = Users.query.filter(Users.user_id != current_user.user_id).all()
        return render_template("allusers.html", users = users)
    else:
        flash('Access denied to requested page', 'danger')
        return redirect(url_for('home.index'))