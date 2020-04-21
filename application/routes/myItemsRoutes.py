import os
from flask import Blueprint, redirect, flash, url_for, render_template, request, jsonify
from flask_login import current_user, login_required
from application import db, app
from application.dbModels.items import Items
from application.routes.indexRoutes import allowed_file

my_items = Blueprint('my_items', __name__)


@my_items.route("/myitems")
@login_required
def myitems():
    items = Items.query.filter_by(user_id=current_user.user_id).all()
    return render_template("my_items.html", items=items, myitems=True)


@my_items.route("/delete_item/<item_id>", methods=['GET'])
@login_required
def delete_item(item_id):
    item = Items.query.filter_by(item_id=item_id).first()
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], item.image_path)):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], item.image_path))
    db.session.delete(item)
    db.session.commit()
    flash('Successfully Deleted', 'success')
    return redirect(url_for('my_items.myitems'))


@my_items.route("/change_item_state/<item_id>/<state>", methods=['GET'])
@login_required
def change_item_state(item_id, state):
    item = Items.query.filter_by(item_id=item_id).first()
    if state == 'inactive':
        item.active = False
    else:
        item.active = True
    db.session.commit()
    flash(f"Item marked {state}", 'success')
    return redirect(url_for('my_items.myitems'))


# TODO: Fix twice image upload
@my_items.route("/get_item_description", methods=['POST'])
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
