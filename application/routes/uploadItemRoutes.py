import os
import time
import uuid
from datetime import datetime

from flask import Blueprint, redirect, flash, url_for, render_template, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from application import db, app
from application.dbModels.items import Items
from application.routes.indexRoutes import allowed_file, LOCATIONS

from ..ml.cv import extract_feature as image_extract_feature  

upload_item = Blueprint('upload_item', __name__)


@upload_item.route("/uploaditem", methods=['POST', 'GET'])
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
            save_fpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_fpath)
            feature_vector, class_label = image_extract_feature(save_fpath)
            feature_vector = list([float(x) for x in feature_vector])
            new_item = Items(current_user.user_id, item_type, location, filename, description, timestamp,
                             feature_vector)
            db.session.add(new_item)
            db.session.commit()
            flash('Item successfully uploaded', 'success')
            return redirect(url_for('my_items.myitems'))
        else:
            flash('Allowed file types are png, jpg, jpeg', 'warning')
            return redirect(request.url), 415
    return render_template("upload.html", date=datetime.now().strftime("%Y-%m-%d"),
                           time=datetime.now().strftime("%H:%M"), locations=LOCATIONS, uploaditem=True)
