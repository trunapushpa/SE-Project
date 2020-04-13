import os
import time
import uuid
from datetime import datetime
import cv2
from PIL import Image
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from application import app, db, login_manager
from flask import render_template, redirect, url_for, session, request, jsonify
from application.dbModels.users import Users
from application.dbModels.items import Items
from application.forms.RegisterForm import RegisterForm
from application.forms.LoginForm import LoginForm
from flask.helpers import flash

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

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route("/")
@app.route("/home")
def index():
    if current_user.is_authenticated:
        return render_template("feed.html", index=True)
    return render_template("landing_page.html", index=True)


@app.route("/switch_theme/<theme>", methods=['POST'])
def switch_theme(theme):
    session['theme'] = theme
    return redirect(request.referrer)


@app.route("/myitems")
@login_required
def myitems():
    return render_template("<h1>No items yet</h1>")


# TODO: Fix twice image upload
@app.route("/get_item_description", methods=['POST'])
@login_required
def get_item_description():
    if 'file' not in request.files:
        return 'File not sent in request', 406
    file = request.files['file']
    if file.filename == '':
        return 'No file uploaded', 406
    if file and allowed_file(file.filename):
        # TODO: Send Real Description instead of file.filename
        return jsonify(description=file.filename)
    else:
        return 'Allowed file types are png, jpg, jpeg', 415


@app.route("/uploaditem", methods=['POST', 'GET'])
@login_required
def uploaditem():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('File not sent in request', 'danger')
            return redirect(request.url), 406
        file = request.files['file']
        if file.filename == '':
            flash('No file uploaded', 'danger')
            return redirect(request.url), 406
        if file and allowed_file(file.filename):
            item_type = request.form['type']
            location = request.form['location']
            description = request.form['description']
            input_date = request.form['date']
            input_time = request.form['time']
            timestamp = time.mktime(time.strptime(input_date + " " + input_time, "%Y-%m-%d %H:%M"))
            filename = secure_filename(str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower())
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # TODO: Find Feature Vector
            feature_vector = [1, 2, 3]
            new_item = Items(current_user.user_id, item_type, location, filename, description, timestamp,
                             feature_vector)
            db.session.add(new_item)
            db.session.commit()
            flash('Item successfully uploaded', 'success')
            return redirect(url_for('index'))
        else:
            flash('Allowed file types are png, jpg, jpeg', 'warning')
            return redirect(request.url), 415
    return render_template("upload.html", date=datetime.now().strftime("%Y-%m-%d"),
                           time=datetime.now().strftime("%H:%M"))


@app.route("/myprofile")
@login_required
def myprofile():
    if session.get('email'):
        data = session
    return render_template("myprofile.html", myprofile=True, data = data)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
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
    if current_user.is_authenticated:
        return redirect('/home')

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
<<<<<<< HEAD
        user = Users.isCredentialsCorrect(email, password)
        if user != None:
            flash(f'Successfully logged in !!', "success")
            session['email'] = user.email
            session['user_id'] = user.user_id
            session['firstName'] = user.first_name
            session['lastName'] = user.last_name
=======
        auth_success, user = Users.isCredentialsCorrect(email, password)
        if auth_success:
            login_user(user)
            flash(f'Successfully logged in !!', "success")
>>>>>>> a03e9c378696dbeee1651f6c9749baefee795934
            return redirect('/home')
        else:
            flash(f'Invalid Username or password. Please try again !!', "danger")
    return render_template("login.html", login=True, form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out", "success")
    return redirect("/home")


@app.errorhandler(Exception)
def all_exception_handler(e):
    return render_template("error.html", error=e), 500
