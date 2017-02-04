from __future__ import absolute_import
from celery import Celery

celery_app = Celery('celery_tasks',
             broker='redis://localhost:6379',
             backend='redis://localhost:6379',
             include=['celery_app.tasks'])

if __name__ == '__main__':
    celery_app.start()
