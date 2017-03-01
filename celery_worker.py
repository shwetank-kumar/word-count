from wordcounter import celery, create_app
from flask import current_app
from config import config

app = create_app('docker')
app.app_context().push()
