from datetime import datetime
from flask_login import login_required, current_user
from flask import render_template, request, jsonify, Blueprint
from application.dbModels.users import Users
from application.dbModels.items import Items
from application.forms.SearchForm import SearchForm

home = Blueprint('home', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
LOCATIONS = ['Himalaya', 'Vindhya', 'KCIS', 'NBH', 'OBH', 'JC', 'Bakul', 'BBC', 'Football Ground', 'Unknown']
TYPES = ['lost', 'found', 'buy', 'sell']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@home.route("/")
@home.route("/home", methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        if request.method == 'GET':
            form = SearchForm()
            items = Items.query.filter(Items.user_id != current_user.user_id).all()
            return render_template("feed.html", index=True, items=items, form=form, locations=LOCATIONS, types=TYPES,
                                   date=datetime.now().strftime("%Y-%m-%d"))
        form = SearchForm()
        search_type = form.search_type.data
        if search_type == 'simple':
            query = form.query.data
            print(query)
        elif search_type == 'adv':
            query = form.query.data
            types = form.types.data
            locations = form.locations.data
            start_date = form.start_date.data
            end_date = form.end_date.data
            print(search_type, query, types, locations, start_date.day, start_date.month, start_date.year)
        elif search_type == 'simple-img':
            # don't know if the following code works
            img = form.img.data
            print(img)
        elif search_type == 'adv-img':
            img = form.img.data
            types = form.types.data
            locations = form.locations.data
            start_date = form.start_date.data
            end_date = form.end_date.data
            print(search_type, types, img)
        items = Items.query.filter_by(location="Himalaya").all()
        new_search_form = SearchForm()
        return render_template("feed.html", index=True, items=items, form=new_search_form, locations=LOCATIONS,
                               types=TYPES, date=datetime.now().strftime("%Y-%m-%d"))
    return render_template("landing_page.html", index=True)


@home.route("/get_contact_info", methods=['POST'])
@login_required
def get_contact_info():
    user_id = request.form['user_id']
    user = Users.query.filter_by(user_id=user_id).first()
    name = user.first_name + " " + user.last_name
    email = user.email
    return jsonify(name=name, email=email)


