from __future__ import absolute_import
from bs4 import BeautifulSoup
from collections import Counter
from .celery import celery_app
import nltk
import re
import requests
from stop_words import stop_wds

nltk.data.path.append('./celery_app/nltk_data/')

@celery_app.task(bind=True)
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
        print word_count
        try:
            result = Result(url=url, redis_id=self.request.id, result_all=word_count,
                            result_no_stop_words=no_stop_words_count)
            db.session.add(result)
            db.session.commit()
            return result.id
        except:
            errors.append('Could not add result to database.')
            return errors
