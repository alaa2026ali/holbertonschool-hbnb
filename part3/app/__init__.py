from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.api.v1 import api_v1_blueprint
from config import config
from flask_jwt_extended import JWTManager

jwt = JWTManager()
db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(config_name='default'):
    app = Flask(__name__)
    # Load configuration
    app.config.from_object(config[config_name])
    # Initialize JWT
    jwt.init_app(app)
    # Initialize SQLAlchemy
    db.init_app(app)
    # Initialize Bcrypt
    bcrypt.init_app(app)
    # Register API v1 blueprint
    app.register_blueprint(api_v1_blueprint)
    return app
