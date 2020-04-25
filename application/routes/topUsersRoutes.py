from flask import Blueprint, render_template

from application.dbModels.users import Users

top_users = Blueprint('top_users', __name__)

ascRankValues = [0, 5, 20, 50, 100]
ascRanks = ['Rookie', 'Beginner', 'Skilled', 'Proficient', 'Expert']
ascRankColors = ['secondary', 'success', 'info', 'warning', 'danger']
REWARD = {'lost': [1, 6], 'found': [6, 1], 'buy': [3, 3], 'sell': [3, 3], 'unsuccessful': 1}


@top_users.route("/top_users")
def top_users_page():
    users = Users.query.order_by(Users.reward.desc()).limit(10).all()
    return render_template("top_users.html", users=users, ascRanks=ascRanks, ascRankColors=ascRankColors,
                           ascRankValues=ascRankValues, reward=REWARD, top_users=True)
