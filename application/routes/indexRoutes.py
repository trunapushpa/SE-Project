from datetime import datetime
import numpy as np
from flask_login import login_required, current_user
from flask import render_template, request, jsonify, Blueprint
from application.dbModels.users import Users
from application.dbModels.items import Items
from application.dbModels.wordVector import WordVector
from application.forms.MessageForm import MessageForm
from application.forms.SearchForm import SearchForm
from .. import app

from ..ml.cv import extract_feature as image_extract_feature

home = Blueprint('home', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
LOCATIONS = ['Himalaya', 'Vindhya', 'KCIS', 'NBH', 'OBH', 'JC', 'Bakul', 'BBC', 'Football Ground', 'Unknown']
TYPES = ['lost', 'found', 'buy', 'sell']
MIN_DATE = '1970-01-01'
MAX_DATE = '2100-01-01'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_text_query(query):
    query_list = query.split()
    result_vector, words = [0] * 300, 0
    for word in query_list:
        results = WordVector.query.filter(WordVector.word == word).all()
        if len(results):
            result_vector = [x + y for (x, y) in zip(result_vector, results[0].vector)]
            words = words + 1
    if words > 0:
        result_vector = [x / words for x in result_vector]
    return result_vector

def process_image_query(image):
    save_fpath = os.path.join(app.config['UPLOAD_FOLDER'], 'query-' + str('-'.join(str(datetime.datetime.now()).split(' '))))
    file.save(save_fpath)
    image_feature_vector, image_text_description = image_extract_feature(save_fpath)
    word_feature_vector = process_text_query(image_text_description)
    return word_feature_vector, image_feature_vector

def MSE(l1, l2):
    l1 = np.asarray(l1)
    l2 = np.asarray(l2)
    return ((l1 - l2) ** 2).mean(axis = 0)

def distance(item, word_vec, image_vec, word_w=1, image_w=1):
    skip = True
    word_distance = 0
    if item.word_vector is not None and word_vec is not None:
        word_distance = MSE(item.word_vector, word_vec)
        skip = False

    image_distance = 0
    if item.feature_vector is not None and image_vec is not None:
        image_distance = MSE(item.feature_vector, image_vec)
        skip = False

    return np.inf if skip else word_w * word_distance + image_w * image_distance


@home.route("/")
@home.route("/home", methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        if request.method == 'GET':
            form = SearchForm()
            new_message_form = MessageForm()
            items = Items.query.filter(Items.user_id != current_user.user_id).all()
            return render_template("feed.html", index=True, items=items, form=form, locations=LOCATIONS, types=TYPES,
                                   date=datetime.now().strftime("%Y-%m-%d"), send_message_form=new_message_form)

        locations = LOCATIONS
        types = TYPES
        start_date = MIN_DATE
        end_date = MAX_DATE
        query_word_vector = None
        query_image_vector = None

        form = SearchForm()
        search_type = form.search_type.data
        if search_type == 'simple':
            query = form.query.data
            query_word_vector = process_text_query(query)
        elif search_type == 'adv':
            query = form.query.data
            types = form.types.data
            locations = form.locations.data
            start_date = form.start_date.data
            end_date = form.end_date.data
            print(search_type, query, types, locations, start_date.day, start_date.month, start_date.year)
            query_word_vector = process_text_query(query)
        elif search_type == 'simple-img':
            # don't know if the following code works
            img = form.img.data
            query_word_vector, query_image_vector = process_image_query(form.img.data)
            print(img)
        elif search_type == 'adv-img':
            img = form.img.data
            types = form.types.data
            locations = form.locations.data
            start_date = form.start_date.data
            end_date = form.end_date.data
            query_word_vector, query_image_vector = process_image_query(form.img.data)
            print(search_type, types, img)
        items = Items.query.filter(
            Items.location.in_(locations),
            Items.type.in_(types),
            Items.timestamp.between(start_date, end_date)).all()
        items.sort(key = lambda item: distance(item, query_word_vector, query_image_vector))
        new_search_form = SearchForm()
        new_message_form = MessageForm()
        return render_template("feed.html", index=True, items=items, form=new_search_form, locations=LOCATIONS,
                               types=TYPES, date=datetime.now().strftime("%Y-%m-%d"),
                               send_message_form=new_message_form)
    return render_template("landing_page.html", index=True)


@home.route("/get_contact_info", methods=['POST'])
@login_required
def get_contact_info():
    user_id = request.form['user_id']
    user = Users.query.filter_by(user_id=user_id).first()
    name = user.first_name + " " + user.last_name
    email = user.email
    rank_id = 0
    for i, rank in enumerate(app.config['ASCRANKVALUES']):
        if user.reward >= rank:
            rank_id = i
    rank_html = "&nbsp;<small><small><span class=\"badge badge-pill badge-" + app.config['ASCRANKCOLORS'][rank_id] + "\">" + app.config['ASCRANKS'][
        rank_id] + "</span></small></small>"
    return jsonify(name=name, email=email, rank=rank_html)
