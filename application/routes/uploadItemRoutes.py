import os
import time
import uuid
from datetime import datetime
from flask import Blueprint, redirect, flash, url_for, render_template, request, jsonify
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from application import db, app
from application.dbModels.items import Items
from application.routes.indexRoutes import allowed_file, LOCATIONS

from ..ml.cv import extract_feature as image_extract_feature  

upload_item = Blueprint('upload_item', __name__)


@upload_item.route("/get_item_description", methods=['POST'])
@login_required
def get_item_description():
    if 'file' not in request.files:
        return 'File not sent in request', 406
    file = request.files['file']
    if file.filename == '':
        return 'No file uploaded', 406
    if file and allowed_file(file.filename):
        filename = secure_filename(str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower())
        save_fpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_fpath)
        feature_vector, class_label = image_extract_feature(save_fpath)
        feature_vector = list([float(x) for x in feature_vector])
        return jsonify(description=class_label, filename=filename, f_vector=feature_vector)
    else:
        return 'Allowed file types are png, jpg, jpeg', 415


@upload_item.route("/uploaditem", methods=['POST', 'GET'])
@login_required
def uploaditem():
    if request.method == 'POST':
        item_type = request.form['type']
        location = request.form['location']
        description = request.form['description']
        input_date = request.form['date']
        input_time = request.form['time']
        filename = request.form['filename']
        f_vector = request.form['f_vector'].split(",")
        feature_vector = [float(i) for i in f_vector]
        timestamp = time.mktime(time.strptime(input_date + " " + input_time, "%Y-%m-%d %H:%M"))
        new_item = Items(current_user.user_id, item_type, location, filename, description, timestamp,
                         feature_vector)
        db.session.add(new_item)
        db.session.commit()
        flash('Item successfully uploaded', 'success')
        return redirect(url_for('my_items.myitems'))
    return render_template("upload.html", date=datetime.now().strftime("%Y-%m-%d"),
                           time=datetime.now().strftime("%H:%M"), locations=LOCATIONS, uploaditem=True)
