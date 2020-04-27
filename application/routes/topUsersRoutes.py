from flask import Blueprint, render_template

from application.dbModels.users import Users

top_users = Blueprint('top_users', __name__)


@top_users.route("/top_users")
def top_users_page():
    users = Users.query.order_by(Users.reward.desc()).limit(10).all()
    return render_template("top_users.html", users=users, top_users=True)
