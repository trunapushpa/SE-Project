from flask import Blueprint, redirect, flash, url_for, render_template, request, Flask
from flask_login import current_user, login_required
#from flask_user import roles_required
from application import db, app
from application.dbModels.items import Items
from application.dbModels.allItems import AllItems

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