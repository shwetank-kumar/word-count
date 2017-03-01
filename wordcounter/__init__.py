from flask import Flask
from config import config
# from config import DevelopmentConfig as SvcsConfig
from config import DockerConfig as SvcsConfig
from celery import Celery
from flask_sqlalchemy import SQLAlchemy

celery = Celery(__name__, broker=SvcsConfig.broker_url,
                backend=SvcsConfig.result_backend)
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
