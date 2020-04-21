from flask import Blueprint, redirect, flash, url_for, render_template
from flask_login import current_user, login_required
from application import db
from application.forms.UpdateNameForm import UpdateNameForm
from application.forms.UpdatePwdForm import UpdatePwdForm

my_profile = Blueprint('my_profile', __name__)


@my_profile.route("/userprofile")
@login_required
def myprofile():
    update_name_form = UpdateNameForm()
    update_pwd_form = UpdatePwdForm()
    return render_template("user_profile.html",
                           update_name_form=update_name_form,
                           update_pwd_form=update_pwd_form,
                           myprofile=True)


@my_profile.route('/updatename', methods=["POST"])
@login_required
def update_name():
    form = UpdateNameForm()
    if form.validate_on_submit():
        user = current_user
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        db.session.add(user)
        db.session.commit()
        flash('Name changed!', 'success')
        return redirect(url_for('my_profile.myprofile'))
    flash('First or Last Name cannot be empty and should not be longer than 50 characters', 'danger')
    return redirect(url_for('my_profile.myprofile'))


@my_profile.route('/password_change', methods=["POST"])
@login_required
def user_password_change():
    form = UpdatePwdForm()
    if form.validate_on_submit():
        user = current_user
        user.pwd = form.password.data
        user.set_password(user.pwd)
        db.session.add(user)
        db.session.commit()
        flash('Password has been updated!', 'success')
        return redirect(url_for('my_profile.myprofile'))
    if not form.password.data == form.confirmPassword.data:
        flash('Password and Confirmed Password does not match!!', 'danger')
    else:
        flash('Password should at least 5 characters long', 'danger')
    return redirect(url_for('my_profile.myprofile'))
