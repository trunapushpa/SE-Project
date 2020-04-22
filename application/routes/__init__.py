import json
from flask import render_template, session, redirect, request
from application import app, db, login_manager
from application.dbModels.users import Users
from application.routes.indexRoutes import home
from application.routes.myItemsRoutes import my_items
from application.routes.myProfileRoutes import my_profile
from application.routes.uploadItemRoutes import upload_item
from application.routes.userRoutes import user
from application.routes.allItemsRoutes import all_items
from application.routes.allUsersRoutes import all_users

app.register_blueprint(home, prefix_url='')
app.register_blueprint(user, prefix_url='')
app.register_blueprint(my_items, prefix_url='')
app.register_blueprint(my_profile, prefix_url='')
app.register_blueprint(upload_item, prefix_url='')
app.register_blueprint(all_items, prefix_url='')
app.register_blueprint(all_users, prefix_url='')


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route("/switch_theme/<theme>", methods=['POST'])
def switch_theme(theme):
    session['theme'] = theme
    return redirect(request.referrer)


@app.route('/about')
def about():
    file = open('team.json', 'r')
    team = json.load(file)
    return render_template('about.html', about=True, team=team)


@app.errorhandler(Exception)
def all_exception_handler(e):
    if e.code and isinstance(e.code, int):
        return render_template("error.html", error=e), e.code
    return render_template("error.html", error=e), 500
