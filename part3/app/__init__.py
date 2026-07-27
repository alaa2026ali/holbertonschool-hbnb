from flask import Flask
from app.api.v1 import api_v1_blueprint

def create_app():
    app = Flask(__name__)

    # Register API v1 blueprint
    app.register_blueprint(api_v1_blueprint)

    return app
