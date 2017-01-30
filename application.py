import nltk
import operator
import re
import requests
from bs4 import BeautifulSoup
from celery import Celery
from celery.result import AsyncResult
from collections import Counter
from config import DevelopmentConfig
from flask import Flask
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request
from stop_words import stop_wds
import time

appl = Flask(__name__)

appl.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(appl)

from models import Result

nltk.data.path.append('./nltk_data/')

celeryd = Celery(appl.name, backend=appl.config['CELERY_RESULT_BACKEND'],
                broker=appl.config['CELERY_BROKER_URL'])

@celeryd.task(bind=True)
def count_and_save_words(self, url):
    errors = []
    print url
    try:
        r = requests.get(url)
    except:
        errors.append('Could not open the URL')

    if r:
        raw_text = BeautifulSoup(r.text, 'html.parser').get_text()
        tokens = nltk.word_tokenize(raw_text)
        text = nltk.Text(tokens)
        non_punct = re.compile('.*[A-Za-z].*')
        raw_words = [w for w in text if non_punct.match(w)]
        word_count = Counter(raw_words)
        no_stop_words = [w for w in raw_words if w.lower() not in stop_wds]
        no_stop_words_count = Counter(no_stop_words)
        # results = sorted(no_stop_words_count.items(), key=operator.itemgetter(1), reverse=True)
        # time.sleep(30)
        try:
            result = Result(url=url, redis_id=self.request.id, result_all=word_count,
                            result_no_stop_words=no_stop_words_count)
            db.session.add(result)
            db.session.commit()
            return result.id
        except:
            errors.append('Could not add result to database.')
            return errors

@appl.route('/', methods=['GET', 'POST'])
def index():
    results = {}
    if request.method == 'POST':
        url = request.form['url']
        if 'http://' not in url[:7]:
            url = 'http://' + url

        task = count_and_save_words.apply_async((url,))
        print task.id
        print task.status
    return render_template('index.html', results=results)


@appl.route("/results/<task_id>", methods=['GET'])
def get_results(task_id):
    result = celeryd.AsyncResult(task_id)
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
