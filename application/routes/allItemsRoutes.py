from flask import Blueprint, redirect, flash, url_for, render_template, request, Flask
from flask_login import current_user, login_required
#from flask_user import roles_required
from application import db, app
from application.dbModels.items import Items
from application.dbModels.allItems import AllItems
import os

all_items = Blueprint('all_items', __name__)

@all_items.route("/allitems", methods=['POST', 'GET'])
@login_required
def allitems():
    if current_user.isadmin:
        #items = Items.query.all()
        items = AllItems.query.all()
        return render_template("allitems.html", items = items)
    else:
        flash('Access denied to requested page', 'danger')
        return redirect(url_for('home.index'))

@all_items.route("/delete_anyitem/<item_id>", methods=['GET'])
@login_required
def delete_anyitem(item_id):
    if current_user.isadmin:
        item = Items.query.filter_by(item_id=item_id).first()
        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], item.image_path)):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], item.image_path))
        db.session.delete(item)
        db.session.commit()
        flash('Successfully Deleted', 'success')
        return redirect(url_for('all_items.allitems'))
    else:
        flash('Access denied to requested page', 'danger')
        return redirect(url_for('home.index'))


@all_items.route("/change_anyitem_state/<item_id>/<state>", methods=['GET'])
@login_required
def change_anyitem_state(item_id, state):
    if current_user.isadmin:
        item = Items.query.filter_by(item_id=item_id).first()
        if state == 'inactive':
            item.active = False
        else:
            item.active = True
        db.session.commit()
        flash(f"Item marked {state}", 'success')
        return redirect(url_for('all_items.allitems'))
    else:
        flash('Access denied to requested page', 'danger')
        return redirect(url_for('home.index'))
