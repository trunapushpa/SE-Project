import os

import cv2
from PIL import Image
from werkzeug.utils import secure_filename

from application import app, db
from flask import render_template, redirect, url_for, session, request
import application.dbModels.users
from application.dbModels.users import Users
from application.dbModels.items import Items
from application.forms.RegisterForm import RegisterForm
from application.forms.LoginForm import LoginForm
from flask.helpers import flash

from application.forms.UploadForm import UploadForm

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# def feature_vector(file):
#     src = cv2.imread(file)
#     target_size = (64, 64)
#     dst = cv2.resize(src, target_size)
#
#     dst = dst.reshape(target_size.shape[0] * target_size.shape[1])
#     return dst


@app.route("/")
@app.route("/home")
def index():
    if session.get('email'):
        return render_template("feed.html", index=True)
    return render_template("landing_page.html", index=True)


@app.route("/switch_theme/<theme>", methods=['POST'])
def switch_theme(theme):
    session['theme'] = theme
    return redirect(request.referrer)


@app.route("/myitems")
def myitems():
    return render_template("<h1>No items yet</h1>")


@app.route("/uploaditem")
def uploadform():
    form = UploadForm()
    return render_template("upload.html", form=form)


@app.route("/uploaditem", methods=['POST'])
def uploaditem():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Incorrect extension')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('NO FILE UPLOADED')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            tag = request.form['tag']
            location = request.form['location']
            caption = request.form['caption']
            # img = Image.open(file)
            # featurevector = feature_vector(file)
            newfile = Items(tag, location, caption, [3, 5])
            filename = secure_filename(file.filename)
            db.session.add(newfile)
            db.session.commit()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect('/home')
        else:
            flash('Allowed file types are png, jpg, jpeg')
            return redirect(request.url)
    return render_template("upload.html")


@app.route("/myprofile")
def myprofile():
    return render_template("<h1>No yet implemented</h1>")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if session.get('email'):
        return redirect('/home')

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        firstname = form.first_name.data
        lastname = form.last_name.data
        password = form.password.data
        newUser = Users(firstname, lastname, email)
        newUser.set_password(password)
        db.session.add(newUser)
        db.session.commit()
        flash(f"Congratulations {firstname}, You are successfully registered.", "success")
        return redirect(url_for('login'))
    return render_template("register.html", register=True, form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if session.get('email'):
        return redirect('/home')

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        if Users.isCredentialsCorrect(email, password):
            flash(f'Successfully logged in !!', "success")
            session['email'] = email
            return redirect('/home')
        else:
            flash(f'Invalid Username or password. Please try again !!', "danger")
    return render_template("login.html", login=True, form=form)


@app.route('/logout')
def logout():
    session['email'] = False
    flash("Logged out", "success")
    return redirect("/home")
