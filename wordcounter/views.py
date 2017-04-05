import operator
from flask import jsonify
from flask import request, render_template
import json
from tasks import count_and_save_words
from wordcounter.config import DevelopmentConfig
from wordcounter import app
from wordcounter.models import Result

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def get_counts():
    data = json.loads(request.data.decode())
    url = data['url']
    print url
    if 'http://' not in url[:7]:
        url = 'http://' + url

    task = count_and_save_words.apply_async((url,))
    print task.id
    return task.id



@app.route("/results/<task_id>", methods=['GET'])
def get_results(task_id):
    result = count_and_save_words.AsyncResult(task_id)
    if result.status == 'SUCCESS':
        result = Result.query.filter_by(redis_id=task_id).first()
        results = sorted(result.result_no_stop_words.items(),
                        key = operator.itemgetter(1),
                        reverse = True)
        return jsonify(results)
    else:
        return result.status, 202
