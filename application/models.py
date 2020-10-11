import flask
from application import db
import datetime

class News(db.Document):
    url = db.StringField(max_length=500, required=True)
    topic = db.StringField(max_length=255, required=False)
    email = db.EmailField(max_length=100, required=False)
    number = db.StringField(max_length=255, required=False)
    submission_time = db.DateTimeField(default=datetime.datetime.utcnow)

class Language(db.Document):
    _id = db.StringField(max_length=255, required=False)
    language = db.StringField(max_length=255, required=False)
