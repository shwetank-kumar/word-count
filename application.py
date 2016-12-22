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
from stop_words import stop_wds

application = Flask(__name__)


application.config.from_object(os.environ['APP_SETTINGS'])
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)

from models import Result

nltk.data.path.append('./nltk_data/')
# stop = set(stopwords.words('english'))


@application.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == 'POST':
        try:
            url = request.form['url']
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
            results = sorted(no_stop_words_count.items(), key=operator.itemgetter(1), reverse=True)
            try:
                result = Result(url=url, result_all=word_count, result_no_stop_words=no_stop_words_count)
                db.session.add(result)
                db.session.commit()
            except:
                errors.append('Could not add result to database.')

    return render_template('index.html', results=results, errors=errors)


if __name__ == '__main__':
    print(os.environ['APP_SETTINGS'])
    application.run()
