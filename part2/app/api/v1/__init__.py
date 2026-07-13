from flask import Blueprint
from flask_restx import Api
from .amenities import api as amenities_ns

from .users import api as users_ns

api_v1_blueprint = Blueprint(
    'api_v1',
    __name__,
    url_prefix='/api/v1'
)

api = Api(
    api_v1_blueprint,
    title='HBnB API',
    version='1.0',
    description='HBnB Application API'
)

api.add_namespace(users_ns, path='/users')
api.add_namespace(amenities_ns, path='/amenities')
