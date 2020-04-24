from flask import Blueprint, redirect, flash, url_for, render_template, request
from flask_login import current_user, login_required
from application import db, app
from application.dbModels.users import Users
from application.forms.UpdatePwdForm import UpdatePwdForm

all_users = Blueprint('all_users', __name__)

@all_users.route('/allusers', methods=['POST', 'GET'])
@login_required
def allusers():
    if current_user.isadmin:
        # Logged in user should not be able to edit his/her account
        users = Users.query.filter(Users.user_id != current_user.user_id).order_by(Users.user_id).all()
        return render_template("allusers.html", users = users)
    else:
        flash('Access denied to requested page', 'danger')
        return redirect(url_for('home.index'))

@all_users.route('/deleteuser/<user_id>', methods=['GET'])
@login_required
def deleteuser(user_id):
    if current_user.isadmin:
        user = Users.query.filter_by(user_id = user_id).first()
        if(user != None):
            db.session.delete(user)
            db.session.commit()
            flash(f'{user.first_name} user deleted successfully.', 'success')
        else:
            flash('Something went wrong..', 'danger')
        return redirect(url_for('all_users.allusers'))
    else:
        flash('Access denied to requested page', 'danger')
        return redirect(url_for('home.index'))

@all_users.route('/changepassword/<user_id>', methods = ['GET'])
@login_required
def changepassword(user_id):
    if current_user.isadmin:
        update_pwd_form = UpdatePwdForm()
        if update_pwd_form.validate_on_submit():
            user = Users.query.filter_by(user_id = user_id).first()   
            if(user != None):
                user.set_password(update_pwd_form.password.data)
                db.session.add(user)
                db.session.commit()
                flash(f'Successfully changed password for {user.first_name}.', 'success')
            else:
                flash('Something went wrong..', 'danger')
            return redirect(url_for('all_users.allusers')) 
    else:
        flash('Access denied to requested page', 'danger')
        return redirect(url_for('home.index'))