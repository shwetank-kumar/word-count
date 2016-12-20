import os
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request
application = Flask(__name__)


application.config.from_object(os.environ['APP_SETTINGS'])
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)

from models import Result


@application.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == 'POST':
        try:
            url = request.form['url']
            r = requests.get(url)
            print(r.text)
        except:
            errors.append('Could not open the URL')

    return render_template('index.html', results=results, errors= errors)


if __name__ == '__main__':
    print(os.environ['APP_SETTINGS'])
    application.run()
