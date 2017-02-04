import nltk
import operator
import re
import requests
from bs4 import BeautifulSoup
# from celery import Celery
# from celery.result import AsyncResult
from celery_app.celery import celery_app
from celery_app import tasks
from collections import Counter
from config import DevelopmentConfig
from flask import Flask
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request
from stop_words import stop_wds
# from tasks import count_and_save_words, celeryd
import time


appl = Flask(__name__)

appl.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(appl)

from models import Result

nltk.data.path.append('./nltk_data/')


@appl.route('/', methods=['GET', 'POST'])
def index():
    results = {}
    if request.method == 'POST':
        url = request.form['url']
        if 'http://' not in url[:7]:
            url = 'http://' + url

        task = tasks.count_and_save_words.apply_async((url,))
        print task.id
        print task.status
    return render_template('index.html', results=results)


@appl.route("/results/<task_id>", methods=['GET'])
def get_results(task_id):
    result = celery_app.AsyncResult(task_id)
    if result.status == 'SUCCESS':
        result = Result.query.filter_by(redis_id=task_id).first()
        results = sorted(result.result_no_stop_words.items(),
                        key = operator.itemgetter(1),
                        reverse = True)
        return jsonify(results)
    else:
        return result.status, 202


if __name__ == '__main__':
    appl.run(host=app.config['HOST'], debug=app.config['DEBUG'])
