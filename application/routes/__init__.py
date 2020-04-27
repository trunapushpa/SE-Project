import json, io, os
from flask import render_template, session, redirect, request, flash
from application import app, db, login_manager
from application.dbModels.users import Users
from application.dbModels.wordVector import WordVector
from application.routes.indexRoutes import home
from application.routes.messageRoutes import message
from application.routes.myItemsRoutes import my_items
from application.routes.myProfileRoutes import my_profile
from application.routes.topUsersRoutes import top_users
from application.routes.uploadItemRoutes import upload_item
from application.routes.userRoutes import user
from application.routes.allItemsRoutes import all_items
from application.routes.allUsersRoutes import all_users

from ..ml.nlp import get_word_list

app.register_blueprint(home, prefix_url='')
app.register_blueprint(user, prefix_url='')
app.register_blueprint(top_users, prefix_url='')
app.register_blueprint(my_items, prefix_url='')
app.register_blueprint(my_profile, prefix_url='')
app.register_blueprint(upload_item, prefix_url='')
app.register_blueprint(message, prefix_url='')
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


# @app.route("/add_vectors", methods=['GET'])
# def save_word_vectors():
    # word_list = get_word_list()
    # print(word_list)
    # WordVector.query.delete()
    # db.session.commit()
    # fname = os.path.join(os.getcwd(), 'application/ml', 'wiki-news-300d-1M-subword.vec')
    # count = 0;
    # with open(fname) as fp:
    #     res = fp.readline()
    #     while True:
    #         res = fp.readline()
    #         if not res:
    #             break;
    #         res = res.split()
    #         w, wv = res[0], []
    #         if w not in word_list:
    #             continue;
    #         for idx in range(1, len(res)):
    #             wv.append(float(res[idx]))
    #         wv_obj = WordVector(w, wv)
    #         count = count + 1
    #         if count % 10 == 0:
    #             db.session.commit()
    #             print('Commit!')
    #         db.session.add(wv_obj)
    #         print('Added:', count)
    # print('Done!', count)
    # db.session.commit()
    # print('Commit!')
    # file = open('team.json', 'r')
    # team = json.load(file)
    # return render_template('about.html', about=True, team=team)


# @app.route("/show_vectors", methods=['GET'])
# def show_word_vectors():
#     res = WordVector.query.all()
#     print(res)
#     flash('Vectors!', 'success')
#     file = open('team.json', 'r')
#     team = json.load(file)
#     return render_template('about.html', about=True, team=team)


@app.errorhandler(Exception)
def all_exception_handler(e):
    if hasattr(e, 'code') and e.code and isinstance(e.code, int):
        return render_template("error.html", error=e), e.code
    return render_template("error.html", error=e), 500
