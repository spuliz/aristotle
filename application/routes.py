from application import app, constants
from flask import render_template, redirect, flash, url_for, request, jsonify
from application.models import News, Language
from datetime import datetime
import requests

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
        if (number)[0:3] == "+39":
           result = "italiano" 
        else:     
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


@app.route('/search', methods=['GET'])
def search():
    if 'query' in request.args:
        query = request.args['query']
    else:
        return jsonify({}), 400

    if 'language' in request.args:
        language = request.args['language']
    else:
        language = 'en-US'

    data = {'key': constants.GOOGLE_API_URL_API_KEY,
            'query': query,
            'languageCode': language,
            }
    # sending get request and saving the response as response object
    r = requests.get(url=constants.GOOGLE_API_BASE_URL, params=data)
    data = r.json()
    # data = jsonify(data) 
    return data, r.status_code


@app.route('/health', methods=['GET'])
def health():
    return jsonify({}), 200
