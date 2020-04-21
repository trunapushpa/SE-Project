from flask import Blueprint, redirect, flash, url_for, render_template
from flask_login import current_user, login_user, login_required, logout_user
from application import db
from application.dbModels.users import Users
from application.forms.LoginForm import LoginForm
from application.forms.RegisterForm import RegisterForm

user = Blueprint('user', __name__)


@user.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/home')

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password = form.password.data
        new_user = Users(first_name, last_name, email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f"Congratulations {first_name}, You are successfully registered.", "success")
        return redirect(url_for('user.login'))
    return render_template("register.html", register=True, form=form)


@user.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        auth_success, cur_user = Users.isCredentialsCorrect(email, password)
        if auth_success:
            login_user(cur_user)
            flash(f'Successfully logged in !!', "success")
            return redirect(url_for('home.index'))
        else:
            flash(f'Invalid Username or password. Please try again !!', "danger")
    return render_template("login.html", login=True, form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out", "success")
    return redirect(url_for('home.index'))
