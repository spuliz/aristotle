from application import app, db
from flask import render_template, redirect, flash, url_for, request, jsonify
from application.models import User, News
<<<<<<< HEAD
from application.forms import LoginForm, RegisterForm, FlagNewsForm
=======
from application.forms import LoginForm, RegisterForm, FlagNews
>>>>>>> 0efd0a6a900530978ab0358becc62554557c2c61
from datetime import datetime


# decorators allow to load function based on webbrowser url mathching those strings
@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def index():
    form = FlagNewsForm()
    if form.validate_on_submit():
<<<<<<< HEAD
=======
        flag_id = News.objects.count()
        flag_id += 1

>>>>>>> 0efd0a6a900530978ab0358becc62554557c2c61
        url = form.url.data
        email = form.email.data
        submission_time = form.submission_time.data

<<<<<<< HEAD
        news = News(submission_time=submission_time, url=url, email=email)
=======
        news = News(flag_id=flag_id, topic=topic, submission_time=submission_time, url=url)
>>>>>>> 0efd0a6a900530978ab0358becc62554557c2c61
        news.save()
        flash("URL successfully flagged!", "success")
        return redirect(url_for('dashboard'))
    return render_template("index.html", index=True, user_login=True, form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # if it does not return error
        email = form.email.data
        password = form.password.data

        # check if email and password are in db
        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f"{user.user_name}, you are successfully logged in!", "success")
            return redirect("/index")  # redirect user to homepage
        else:
            flash("Sorry, something went wrong.", "danger")
    return render_template("login.html", title="Login", form=form, login=True)


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    news = News.objects.order_by("-submission_time")
    count = News.objects.aggregate([{'$group': {
        '_id': "$url",
        'count': {'$sum': 1}
    }
    },
        {
            '$sort': {"count": -1}
        }
    ]
    )

    return render_template("dashboard.html", dashboard=True, data=news, count=count)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count()
        user_id += 1  # add a new ID

        email = form.email.data
        password = form.password.data
        user_name = form.user_name.data

        user = User(user_id=user_id, email=email, user_name=user_name)
        user.set_password(password)
        user.save()
        flash("You are successfully registered!", "success")
        return redirect(url_for('index'))

    return render_template("register.html", title="Register", form=form, register=True)


<<<<<<< HEAD
def isBlank(string):
    return not (string and string.strip())


def isNotBlank(string):
    return bool(string and string.strip())


@app.route('/save', methods=['POST'])
def create():
    from_number = request.json.get('from_number', '')
=======
@app.route('/magic', methods=['POST'])
def create():
    flag_id = News.objects.count()
    flag_id += 1

>>>>>>> 0efd0a6a900530978ab0358becc62554557c2c61
    url = request.json.get('url', '')
    topic = request.json.get('topic', '')
    submission_time = request.json.get('submission_time', datetime.now())

<<<<<<< HEAD
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


@app.route('/query', methods=['POST'])
def query():
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
=======
    news = News(flag_id=flag_id, topic=topic, submission_time=submission_time, url=url)
    news.save()
    flash("URL successfully flagged!", "success")

    count = News.objects().filter(url=url).count()

    return jsonify({'news': news, 'count': count}), 201
>>>>>>> 0efd0a6a900530978ab0358becc62554557c2c61
