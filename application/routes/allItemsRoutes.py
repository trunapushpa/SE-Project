from flask import Blueprint, redirect, flash, url_for, render_template, request, Flask
from flask_login import current_user, login_required
from application.dbModels.allItems import AllItems

from application.routes.myItemsRoutes import delete_item, change_item_state

all_items = Blueprint('all_items', __name__)


@all_items.route("/allitems", methods=['POST', 'GET'])
@login_required
def allitems():
    if current_user.isadmin:
        items = AllItems.query.all()
        return render_template("allitems.html", items = items)
    else:
        flash('Access denied to requested page', 'danger')
        return redirect(url_for('home.index'))


@all_items.route("/delete_anyitem/<item_id>", methods=['GET'])
@login_required
def delete_anyitem(item_id):
    if current_user.isadmin:
        return delete_item(item_id)
    else:
        flash('Access denied to requested page', 'danger')
        return redirect(url_for('home.index'))


@all_items.route("/change_anyitem_state/<item_id>/<state>", methods=['GET'])
@login_required
def change_anyitem_state(item_id, state):
    if current_user.isadmin:
        return change_item_state(item_id, state)
    else:
        flash('Access denied to requested page', 'danger')
        return redirect(url_for('home.index'))
