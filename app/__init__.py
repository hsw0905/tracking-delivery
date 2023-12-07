import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.api.views import api
from app.config import config, Config
from app.extensions.database import db


def init_config(app: Flask, config_name: str):
    app_config: Config = config[config_name]
    app.config.from_object(app_config)


def init_db(app: Flask, database: SQLAlchemy) -> None:
    app.config['SQLALCHEMY_ECHO'] = False
    database.init_app(app)


def init_blueprint(app: Flask):
    app.register_blueprint(api)


def create_app(config_name: str = "default") -> Flask:
    app = Flask(__name__)

    if os.getenv("FLASK_CONFIG") and os.getenv("FLASK_CONFIG") != config_name:
        config_name = os.getenv("FLASK_CONFIG")

    init_config(app, config_name)

    with app.app_context():
        init_blueprint(app)
        init_db(app, db)
        # init_provider()

    print(f"\n💌💌💌Flask Config is '{config_name}'")
    return app
