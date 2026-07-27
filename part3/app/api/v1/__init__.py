from flask import Blueprint
from flask_restx import Api


from .users import api as users_ns
from .amenities import api as amenities_ns
from .places import api as places_ns
from .reviews import api as reviews_ns

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
api.add_namespace(places_ns, path="/places")
api.add_namespace(reviews_ns, path="/reviews")
