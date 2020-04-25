import os
from flask import Blueprint, redirect, flash, url_for, render_template, request, jsonify
from flask_login import current_user, login_required
from application import db, app
from application.dbModels.items import Items
from application.dbModels.users import Users
from application.forms.markInactiveForm import MarkInactiveForm
from application.routes.indexRoutes import allowed_file
from application.routes.topUsersRoutes import REWARD

my_items = Blueprint('my_items', __name__)


@my_items.route("/myitems")
@login_required
def myitems():
    items = Items.query.filter_by(user_id=current_user.user_id).all()
    return render_template("my_items.html", items=items, myitems=True, mark_inactive_form=MarkInactiveForm())


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


@my_items.route("/mark_inactive", methods=['POST'])
def mark_inactive():
    form = MarkInactiveForm()
    form.success.choices = ['Yes', 'No']
    if form.validate_on_submit():
        item_id = form.item_id.data
        item = Items.query.filter_by(item_id=item_id).first()
        if form.success.data == 'Yes':
            user2 = Users.query.filter_by(email=form.email.data).first()
            if not user2:
                flash('No such user found!!', 'danger')
                return redirect(request.referrer)
            if user2.email == current_user.email:
                flash('Nice try ;)', 'warning')
                return redirect(request.referrer)
            current_user.reward += REWARD[item.type][0]
            user2.reward += REWARD[item.type][1]
        else:
            current_user.reward += REWARD['unsuccessful']
        item.active = False
        db.session.commit()
        flash('Item marked inactive', 'success')
    else:
        flash('Wrong form data', 'danger')
    return redirect(request.referrer)


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
