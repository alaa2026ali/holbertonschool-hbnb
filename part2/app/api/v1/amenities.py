from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'id': fields.String(readOnly=True, description='The unique identifier of the amenity'),
    'name': fields.String(required=True, description='Name of the amenity')
})

amenity_create_model = api.model('AmenityCreate', {
    'name': fields.String(required=True, description='Name of the amenity')
})

amenity_update_model = api.model('AmenityUpdate', {
    'name': fields.String(description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):

    @api.marshal_list_with(amenity_model)
    def get(self):
        """Retrieve all amenities"""
        return facade.get_all_amenities(), 200

    @api.expect(amenity_create_model)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        amenity_data = api.payload
        amenity = facade.create_amenity(amenity_data)
        return amenity, 201


@api.route('/<string:amenity_id>')
@api.response(404, 'Amenity not found')
class AmenityResource(Resource):

    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Get amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity, 200

    @api.expect(amenity_update_model)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id):
        """Update an amenity"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")

        facade.update_amenity(amenity_id, api.payload)
        return facade.get_amenity(amenity_id), 200
