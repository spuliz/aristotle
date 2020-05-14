import flask
from application import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Document):
    user_id = db.IntField(unique=True)
    user_name = db.StringField(max_length=50, required=True)
    email = db.StringField(max_length=50, required=True, unique=True)
    password = db.StringField()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)


class Report(db.EmbeddedDocument):
    email = db.EmailField(max_length=100, required=False)
    number = db.StringField(max_length=255, required=False)


class News(db.Document):
    url = db.StringField(max_length=500, required=True)
    topic = db.StringField(max_length=255, required=False)
    report = db.EmbeddedDocumentField(Report)
    submission_time = db.DateTimeField(default=datetime.datetime.utcnow)


class NewsCount(db.Document):
    url = db.StringField(max_length=500, required=True)
    count = db.IntField()
