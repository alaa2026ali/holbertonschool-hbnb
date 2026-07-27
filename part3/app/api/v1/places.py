from flask_restx import Namespace, Resource, fields

from app.services import facade


api = Namespace("places", description="Place operations")


owner_model = api.model("PlaceOwner", {
    "id": fields.String(
        readOnly=True,
        description="The unique identifier of the owner"
    ),
    "first_name": fields.String(
        description="First name of the owner"
    ),
    "last_name": fields.String(
        description="Last name of the owner"
    ),
    "email": fields.String(
        description="Email address of the owner"
    )
})


place_amenity_model = api.model("PlaceAmenity", {
    "id": fields.String(
        readOnly=True,
        description="The unique identifier of the amenity"
    ),
    "name": fields.String(
        description="Name of the amenity"
    )
})


amenity_reference_model = api.model("AmenityReference", {
    "id": fields.String(
        required=True,
        description="The unique identifier of the amenity"
    )
})


place_model = api.model("Place", {
    "id": fields.String(
        readOnly=True,
        description="The unique identifier of the place"
    ),
    "title": fields.String(
        description="Title of the place"
    ),
    "description": fields.String(
        description="Description of the place"
    ),
    "price": fields.Float(
        description="Price per night"
    ),
    "latitude": fields.Float(
        description="Latitude of the place"
    ),
    "longitude": fields.Float(
        description="Longitude of the place"
    ),
    "owner": fields.Nested(owner_model),
    "amenities": fields.List(
        fields.Nested(place_amenity_model)
    )
})


place_create_model = api.model("PlaceCreate", {
    "title": fields.String(
        required=True,
        description="Title of the place"
    ),
    "description": fields.String(
        description="Description of the place"
    ),
    "price": fields.Float(
        required=True,
        description="Price per night"
    ),
    "latitude": fields.Float(
        required=True,
        description="Latitude between -90 and 90"
    ),
    "longitude": fields.Float(
        required=True,
        description="Longitude between -180 and 180"
    ),
    "owner_id": fields.String(
        required=True,
        description="The unique identifier of the owner"
    ),
    "amenities": fields.List(
        fields.Nested(amenity_reference_model),
        description="Amenities associated with the place"
    )
})


place_update_model = api.model("PlaceUpdate", {
    "title": fields.String(
        description="Title of the place"
    ),
    "description": fields.String(
        description="Description of the place"
    ),
    "price": fields.Float(
        description="Price per night"
    ),
    "latitude": fields.Float(
        description="Latitude between -90 and 90"
    ),
    "longitude": fields.Float(
        description="Longitude between -180 and 180"
    )
})


@api.route("/")
class PlaceList(Resource):

    @api.marshal_list_with(place_model)
    def get(self):
        """Retrieve the list of all places."""
        return facade.get_all_places(), 200

    @api.expect(place_create_model, validate=True)
    @api.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place."""
        place_data = api.payload

        try:
            place = facade.create_place(place_data.copy())
            return place, 201

        except (ValueError, KeyError) as error:
            api.abort(400, str(error))


@api.route("/<string:place_id>")
@api.response(404, "Place not found")
class PlaceResource(Resource):

    @api.marshal_with(place_model)
    def get(self, place_id):
        """Retrieve a place by ID."""
        place = facade.get_place(place_id)

        if not place:
            api.abort(404, "Place not found")

        return place, 200

    @api.expect(place_update_model, validate=True)
    @api.marshal_with(place_model)
    def put(self, place_id):
        """Update an existing place."""
        place = facade.get_place(place_id)

        if not place:
            api.abort(404, "Place not found")

        try:
            facade.update_place(place_id, api.payload)
            return facade.get_place(place_id), 200

        except (ValueError, KeyError) as error:
            api.abort(400, str(error))

@api.route("/<string:place_id>/reviews")
@api.response(404, "Place not found")
class PlaceReviewList(Resource):

    def get(self, place_id):
        """Retrieve all reviews for a specific place."""
        try:
            reviews = facade.get_reviews_by_place(place_id)
        except KeyError:
            api.abort(404, "Place not found")

        return [
            {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": review.user.id,
                "place_id": review.place.id
            }
            for review in reviews
        ], 200