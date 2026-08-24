from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import config

jwt = JWTManager()
db = SQLAlchemy()
bcrypt = Bcrypt()

from app.api.v1 import api_v1_blueprint


def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)

    jwt.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        db.create_all()

        from app.seed import seed_data
        seed_data()

    app.register_blueprint(api_v1_blueprint)

    return app
