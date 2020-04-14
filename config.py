import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secret_string"
    # add DB connection here
    MONGODB_SETTINGS = {'db' : 'UTA_Test'}