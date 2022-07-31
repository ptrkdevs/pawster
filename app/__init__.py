from sys import prefix
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
import re

from dotenv import load_dotenv

load_dotenv()

uri = os.environ.get("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

login_manager = LoginManager()

login_manager.login_view = "auth.login"

migrate = Migrate()

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(config_file=None):

    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # db
    db.init_app(app)

    # flask login
    login_manager.init_app(app)

    # flask migrate
    Migrate(app, db)

    # model
    from app.models import User, Pet, Images

    # routes

    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp)

    from app.core import bp as core_bp

    app.register_blueprint(core_bp)

    from app.error.routes import page_not_found

    app.register_error_handler(404, page_not_found)

    return app
