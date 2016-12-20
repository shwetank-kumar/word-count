import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
application = Flask(__name__)


application.config.from_object(os.environ['APP_SETTINGS'])
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)

from models import Result


@application.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    print(os.environ['APP_SETTINGS'])
    application.run()
