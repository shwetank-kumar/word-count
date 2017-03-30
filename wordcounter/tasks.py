from bs4 import BeautifulSoup
from celery import Celery
import nltk
import re
import requests
from collections import Counter
import os
from stop_words import stop_wds
from config import *
from models import Result
from wordcounter import db

pwd = os.path.dirname(os.path.abspath(__file__))

nltk.data.path.append(pwd + '/data/nltk_data/')

celery = Celery(__name__, broker=DevelopmentConfig.broker_url,
                backend=DevelopmentConfig.result_backend)

@celery.task(bind=True)
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

        # print db
        # print url
        # print self.request.id
        # print word_count
        # print no_stop_words

        try:
            result = Result(url=url, redis_id=self.request.id, result_all=word_count,
                            result_no_stop_words=no_stop_words_count)
            db.session.add(result)
            db.session.commit()
            return result.id
        except:
            errors.append('Could not add result to database.')
            return errors
