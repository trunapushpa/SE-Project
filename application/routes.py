from application import app, db
from flask import render_template, redirect, url_for, session
import application.dbModels.users
from application.dbModels.users import Users
from application.forms.RegisterForm import RegisterForm
from application.forms.LoginForm import LoginForm
from flask.helpers import flash

@app.route("/")
@app.route("/home")
def index():
    return render_template("helloWorld.html", index = True)

@app.route("/myitems")
def myitems():
    return render_template("<h1>No items yet</h1>")

@app.route("/uploaditem")
def uploaditem():
    return render_template("<h1>No yet implemented</h1>")

@app.route("/myprofile")
def myprofile():
    if session.get('email'):
        data = session
    return render_template("myprofile.html", myprofile=True, data = data)

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if session.get('email'):
        return redirect('/home')
        
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        firstname = form.first_name.data
        lastname = form.last_name.data
        password = form.password.data
        newUser = Users(firstname,lastname, email)
        newUser.set_password(password)
        db.session.add(newUser)
        db.session.commit()
        flash(f"Congratulations {firstname}, You are successfully registered.", "success")
        return redirect(url_for('login'))
    return render_template("register.html", register = True, form = form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if session.get('email'):
        return redirect('/home')

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = Users.isCredentialsCorrect(email, password)
        if user != None:
            flash(f'Successfully logged in !!', "success")
            session['email'] = user.email
            session['user_id'] = user.user_id
            session['firstName'] = user.first_name
            session['lastName'] = user.last_name
            return redirect('/home')
        else:
            flash(f'Invalid Username or password. Please try again !!', "danger")
    return render_template("login.html", login = True, form = form)

@app.route('/logout')
def logout():
    session['email'] = False
    flash("Logged out", "success")
    return redirect("/home")