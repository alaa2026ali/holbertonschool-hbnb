from flask_restx import Namespace, Resource, fields

from app.services import facade


api = Namespace("reviews", description="Review operations")


review_user_model = api.model("ReviewUser", {
    "id": fields.String(
        readOnly=True,
        description="The unique identifier of the user"
    ),
    "first_name": fields.String(
        description="First name of the user"
    ),
    "last_name": fields.String(
        description="Last name of the user"
    ),
    "email": fields.String(
        description="Email address of the user"
    )
})


review_place_model = api.model("ReviewPlace", {
    "id": fields.String(
        readOnly=True,
        description="The unique identifier of the place"
    ),
    "title": fields.String(
        description="Title of the place"
    )
})


review_model = api.model("Review", {
    "id": fields.String(
        readOnly=True,
        description="The unique identifier of the review"
    ),
    "text": fields.String(
        description="Text of the review"
    ),
    "rating": fields.Integer(
        description="Rating between 1 and 5"
    ),
    "user": fields.Nested(review_user_model),
    "place": fields.Nested(review_place_model)
})


review_create_model = api.model("ReviewCreate", {
    "text": fields.String(
        required=True,
        description="Text of the review"
    ),
    "rating": fields.Integer(
        required=True,
        description="Rating between 1 and 5"
    ),
    "user_id": fields.String(
        required=True,
        description="The unique identifier of the user"
    ),
    "place_id": fields.String(
        required=True,
        description="The unique identifier of the place"
    )
})


review_update_model = api.model("ReviewUpdate", {
    "text": fields.String(
        description="Text of the review"
    ),
    "rating": fields.Integer(
        description="Rating between 1 and 5"
    )
})


@api.route("/")
class ReviewList(Resource):

    @api.marshal_list_with(review_model)
    def get(self):
        """Retrieve the list of all reviews."""
        return facade.get_all_reviews(), 200

    @api.expect(review_create_model, validate=True)
    @api.marshal_with(review_model, code=201)
    def post(self):
        """Create a new review."""
        review_data = api.payload

        try:
            review = facade.create_review(review_data.copy())
            return review, 201

        except (ValueError, KeyError) as error:
            api.abort(400, str(error))


@api.route("/<string:review_id>")
@api.response(404, "Review not found")
class ReviewResource(Resource):

    @api.marshal_with(review_model)
    def get(self, review_id):
        """Retrieve a review by ID."""
        review = facade.get_review(review_id)

        if not review:
            api.abort(404, "Review not found")

        return review, 200

    @api.expect(review_update_model, validate=True)
    @api.marshal_with(review_model)
    def put(self, review_id):
        """Update an existing review."""
        review = facade.get_review(review_id)

        if not review:
            api.abort(404, "Review not found")

        try:
            facade.update_review(review_id, api.payload)
            return facade.get_review(review_id), 200

        except (ValueError, KeyError) as error:
            api.abort(400, str(error))

    @api.response(204, "Review deleted")
    def delete(self, review_id):
        """Delete a review."""
        review = facade.get_review(review_id)

        if not review:
            api.abort(404, "Review not found")

        try:
            facade.delete_review(review_id)
            return "", 204

        except KeyError as error:
            api.abort(404, str(error))