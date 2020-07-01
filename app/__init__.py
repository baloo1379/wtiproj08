from flask import Flask
from app.models import db


class Config(object):
    SECRET_KEY = 'dev',

    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'

    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config())

db.init_app(app)

with app.app_context():
    from . import models, controllers, services

    db.create_all()
    models.init_app(app)
    controllers.init_app(app)
    services.init_app(app)
