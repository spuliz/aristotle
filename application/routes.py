from application import app, db
from flask import render_template, redirect, flash, url_for, request, jsonify
from application.models import News, Language
from application.forms import LoginForm, RegisterForm, FlagNewsForm
from datetime import datetime
import requests


# decorators allow to load function based on webbrowser url mathching those strings
# @app.route("/", methods=['GET', 'POST'])
# @app.route("/index", methods=['GET', 'POST'])
# @app.route("/home", methods=['GET', 'POST'])
# def index():
#     form = FlagNewsForm()
#     if form.validate_on_submit():
#         url = form.url.data
#         email = form.email.data
#         submission_time = form.submission_time.data
#
#         news = News(submission_time=submission_time, url=url, email=email)
#         news.save()
#         flash("URL successfully flagged!", "success")
#         return redirect(url_for('dashboard'))
#     return render_template("index.html", index=True, user_login=True, form=form)


# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():  # if it does not return error
#         email = form.email.data
#         password = form.password.data
#
#         # check if email and password are in db
#         user = User.objects(email=email).first()
#         if user and user.get_password(password):
#             flash(f"{user.user_name}, you are successfully logged in!", "success")
#             return redirect("/index")  # redirect user to homepage
#         else:
#             flash("Sorry, something went wrong.", "danger")
#     return render_template("login.html", title="Login", form=form, login=True)


# @app.route("/dashboard", methods=['GET', 'POST'])
# def dashboard():
#     news = News.objects.order_by("-submission_time")
#     count = News.objects.aggregate([{'$group': {
#         '_id': "$url",
#         'count': {'$sum': 1}
#     }
#     },
#         {
#             '$sort': {"count": -1}
#         }
#     ]
#     )
#
#     return render_template("dashboard.html", dashboard=True, data=news, count=count)


# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         user_id = User.objects.count()
#         user_id += 1  # add a new ID
#
#         email = form.email.data
#         password = form.password.data
#         user_name = form.user_name.data
#
#         user = User(user_id=user_id, email=email, user_name=user_name)
#         user.set_password(password)
#         user.save()
#         flash("You are successfully registered!", "success")
#         return redirect(url_for('index'))
#
#     return render_template("register.html", title="Register", form=form, register=True)

@app.errorhandler(404)
def page_not_found(e):
    return redirect("https://www.twidia.org/", code=302)


def isBlank(string):
    return not (string and string.strip())


def isNotBlank(string):
    return bool(string and string.strip())


@app.route('/url', methods=['POST'])
def save_report():
    from_number = request.json.get('number', '')
    url = request.json.get('url', '')
    topic = request.json.get('topic', '')
    submission_time = request.json.get('submission_time', datetime.now())

    news = News(topic=topic, submission_time=submission_time, url=url,
                number=from_number)
    news.save()
    flash("URL successfully flagged!", "success")

    pipeline = [
        {"$match": {
            "url": url,
            "number": {"$ne": from_number}
        }}, {"$group": {"_id": "$number", "count": {"$sum": 1}}},
    ]

    result = list(News.objects().aggregate(pipeline))

    # cursorlist = [c for c in result]
    # print(cursorlist)

    return jsonify({'news': news, 'count': len(result)}), 201


@app.route('/url/query', methods=['POST'])
def query_top():
    limit = request.json.get('top', 3)

    pipeline = [
        {"$group": {"_id": {"number": "$number", "url": "$url"}}},
        {"$group": {"_id": "$_id.url", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]

    result = list(News.objects().aggregate(pipeline))

    cursorlist = [c for c in result]

    return jsonify(cursorlist), 200


@app.route('/language', methods=['GET'])
def get_language():
    if 'number' in request.args:
        number = request.args['number']
    else:
        return jsonify({}), 400

    try:
        variable = Language.objects.get(_id=number)
        result = variable.language
    except Language.DoesNotExist:
        result = "english"
    return jsonify({'language': result}), 200


@app.route('/language', methods=['POST'])
def save_language():
    language = request.json.get('language', '')
    number = request.json.get('number', '')

    # _id field is indexed primary key represented by number, saving and update  is automatic by number
    lan = Language(_id=number, language=language)
    lan.save()
    flash("Language successfully saved", "success")

    return jsonify({'language': language}), 200


# api-endpoint
URL = "https://content-factchecktools.googleapis.com/v1alpha1/claims:search"
API_KEY = ""


@app.route('/search', methods=['GET'])
def search():
    # data to be sent to api
    if 'query' in request.args:
        query = request.args['query']
    else:
        return jsonify({}), 400

    data = {'key': API_KEY,
            'query': query}
    # sending get request and saving the response as response object
    r = requests.get(url=URL, params=data)
    data = r.json()

    return jsonify(data), r.status_code
