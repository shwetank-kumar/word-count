from . import webapp
from .tasks import count_and_save_words
from flask import request, render_template
# from .models import Result


@webapp.route('/', methods=['GET', 'POST'])
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


@webapp.route("/results/<task_id>", methods=['GET'])
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
