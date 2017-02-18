from flask import Flask
from config import config, DevelopmentConfig
from celery import Celery
from flask_sqlalchemy import SQLAlchemy

celery = Celery(__name__, broker=DevelopmentConfig.broker_url,
                backend=DevelopmentConfig.result_backend)
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    celery.conf.update(app.config)

    from .webapp import webapp
    app.register_blueprint(webapp)

    return app
