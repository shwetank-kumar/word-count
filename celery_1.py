from celery import Celery

app = Celery('celery_1', backend='rpc://', broker='amqp://user:password@127.0.0.1:8080/')


@app.task
def add(x, y):
    return x + y
