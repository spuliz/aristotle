import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secret_string"
    # add DB connection here
    MONGODB_SETTINGS = {
        'host': 'mongodb+srv://twidia:Kalispera2020@cluster0-3skvg.mongodb.net/whatsapp_db?retryWrites=true&w=majority',
        'db' : 'whatsapp_db'
        }
