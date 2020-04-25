from flask import Blueprint, redirect, flash, url_for, render_template, request
from flask_login import current_user, login_required
from application import db, app
from application.dbModels.users import Users
from application.forms.UpdatePwdForm import UpdatePwdForm
from application.forms.NewUserForm import NewUserForm

all_users = Blueprint('all_users', __name__)


@all_users.route('/allusers', methods=['POST', 'GET'])
@login_required
def allusers():
    if current_user.isadmin:
        update_pwd_form = UpdatePwdForm()
        new_user_form = NewUserForm()
        # Logged in user should not be able to edit his/her account
        users = Users.query.filter(Users.user_id != current_user.user_id).order_by(Users.user_id.asc()).all()
        return render_template("allusers.html", users = users, update_pwd_form = update_pwd_form, form = new_user_form)
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

@all_users.route('/changepassword/<user_id>', methods = ['POST'])
@login_required
def changepassword(user_id):
    if current_user.isadmin:
        form = UpdatePwdForm()
        if form.validate_on_submit():
            user = Users.query.filter_by(user_id = user_id).first()   
            if(user != None):
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                flash(f'Successfully changed password for {user.first_name}.', 'success')
            else:
                flash('Something went wrong..', 'danger')
        if not form.password.data == form.confirmPassword.data:
            flash('Password and Confirmed Password does not match!!', 'danger')
        return redirect(url_for('all_users.allusers')) 
    else:
        flash('Access denied to requested page', 'danger')
    return redirect(url_for('home.index'))

@all_users.route("/newuser", methods=["POST"])
@login_required
def newuser():
    if current_user.isadmin:
        user_form = NewUserForm()
        if user_form.validate_on_submit():
            email = user_form.email.data
            first_name = user_form.first_name.data
            last_name = user_form.last_name.data
            password = user_form.password.data
            new_user = Users(first_name, last_name, email)
            new_user.isadmin = user_form.isAdmin.data
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash(f"User successully created.", "success")
        else:
            if not user_form.errors == None:
                for error in user_form.errors:
                    flash(f"{error} : {user_form.errors[error]}", "danger")
        return redirect(url_for('all_users.allusers'))
    else:
        flash('Access denied to requested page', 'danger')
    return redirect(url_for('home.index'))