from flask import url_for, flash, jsonify, Blueprint, redirect, request, render_template
from flask_login import login_required, current_user
from datetime import datetime
from application import db
from application.dbModels.message import Messages
from application.dbModels.notification import Notification
from application.dbModels.users import Users
from application.forms.MessageForm import MessageForm

message = Blueprint('message', __name__)


@message.route('/send_message/<recipient>', methods=['POST'])
@login_required
def send_message(recipient):
    msg_receiver = Users.query.filter_by(user_id=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Messages(author=current_user, recipient=msg_receiver, body=form.message.data, item_id=form.item_id.data)
        msg_receiver.add_notification('unread_message_count', msg_receiver.new_messages())
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent.', 'success')
    return redirect(request.referrer)


@message.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.now()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    msgs = current_user.messages_received.order_by(
        Messages.timestamp.desc()).paginate(
            page, 3, False)
    next_url = url_for('message.messages', page=msgs.next_num) \
        if msgs.has_next else None
    prev_url = url_for('message.messages', page=msgs.prev_num) \
        if msgs.has_prev else None
    return render_template('messages.html', messages=msgs.items,
                           next_url=next_url, prev_url=prev_url, send_message_form=MessageForm())


@message.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    since = datetime.fromtimestamp(since/1000)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])
