import flask 
from application import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Document):
    user_id  = db.IntField( unique=True )
    user_name = db.StringField( max_length=50, required=True )
    email = db.StringField( max_length=50, required = True, unique=True )
    password = db.StringField()

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def get_password(self, password):
        return check_password_hash(self.password, password)

class News(db.Document):
    flag_id = db.IntField( unique=True )
    url = db.StringField(max_length=500, required=True)
    topic = db.StringField(max_length=255, required=True)
    submission_time = db.DateTimeField(default=datetime.datetime.utcnow)

class NewsCount(db.Document):
    url = db.StringField(max_length=500, required=True)
    count = db.IntField()



# class User_History(db.Document):
#     # which urls has the user submitted
#     user_id = db.IntField( unique=True ) #primary key to join with user table 
#     #flag_id = db.IntField( unique=True ) # primry key to join with news table  
#     url = db.StringField(max_length=500, required=True)