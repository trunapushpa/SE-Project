import json
from flask import render_template, session, redirect, request, url_for, flash, current_app
from flask_login import login_required, current_user
from datetime import datetime
from application import app, db, login_manager
from application.dbModels.message import Messages
from application.dbModels.users import Users
from application.forms.MessageForm import MessageForm
from application.routes.indexRoutes import home
from application.routes.myItemsRoutes import my_items
from application.routes.myProfileRoutes import my_profile
from application.routes.uploadItemRoutes import upload_item
from application.routes.userRoutes import user

app.register_blueprint(home, prefix_url='')
app.register_blueprint(user, prefix_url='')
app.register_blueprint(my_items, prefix_url='')
app.register_blueprint(my_profile, prefix_url='')
app.register_blueprint(upload_item, prefix_url='')


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
    if hasattr(e, 'code') and e.code and isinstance(e.code, int):
        return render_template("error.html", error=e), e.code
    return render_template("error.html", error=e), 500


@app.route('/send_message/<recipient>', methods=['POST'])
@login_required
def send_message(recipient):
    msgReciever = Users.query.filter_by(user_id=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Messages(author=current_user, recipient=msgReciever,
                       body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent.', 'success')
    return redirect(url_for('home.index'))


@app.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.now()
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    msgs = current_user.messages_received.order_by(
        Messages.timestamp.desc()).paginate(
            page, 3, False)
    next_url = url_for('messages', page=msgs.next_num) \
        if msgs.has_next else None
    prev_url = url_for('messages', page=msgs.prev_num) \
        if msgs.has_prev else None
    return render_template('messages.html', messages=msgs.items,
                           next_url=next_url, prev_url=prev_url)