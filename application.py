import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
application = Flask(__name__)


application.config.from_object(os.environ['APP_SETTINGS'])
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)

from models import Result


@application.route('/')
def hello():
    return "Hello World!"


@application.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    print(os.environ['APP_SETTINGS'])
    application.run()
