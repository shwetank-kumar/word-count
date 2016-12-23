import nltk
import operator
import os
import re
import requests
from bs4 import BeautifulSoup
from collections import Counter
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request
from rq import Queue
from rq.job import Job
from stop_words import stop_wds
from worker import conn

application = Flask(__name__)


application.config.from_object(os.environ['APP_SETTINGS'])
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(application)

q = Queue(connection=conn)

from models import *

nltk.data.path.append('./nltk_data/')
# stop = set(stopwords.words('english'))


@application.route('/', methods=['GET', 'POST'])
def index():
    results = {}
    if request.method == 'POST':
        url = request.form['url']
        if 'http://' not in url[:7]:
            url = 'http://' + url

        job = q.enqueue_call(func=count_and_save_words, args=(url, ), result_ttl=5000)
        print(job.get_id())

    return render_template('index.html', results=results)






def count_and_save_words(url):
    errors = []

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
        try:
            result = Result(url=url, result_all=word_count, result_no_stop_words=no_stop_words_count)
            db.session.add(result)
            db.session.commit()
            return result.id
        except:
            errors.append('Could not add result to database.')
            return errors






if __name__ == '__main__':
    print(os.environ['APP_SETTINGS'])
    application.run()
