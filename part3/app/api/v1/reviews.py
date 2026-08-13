from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
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
    @jwt_required()
    def post(self):
        """Create a new review."""

        review_data = api.payload.copy()

        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")

        # Check that the user exists
        user = facade.get_user(user_id)

        if not user:
            api.abort(400, "User not found")

        # Check that the place exists
        place = facade.get_place(place_id)

        if not place:
            api.abort(400, "Place not found")

        # Prevent user from reviewing their own place
        if place.owner.id == user_id:
            api.abort(400, "You cannot review your own place")

        # Prevent duplicate reviews
        reviews = facade.get_reviews_by_place(place_id)

        for review in reviews:
            if review.user.id == user_id:
                api.abort(400, "You have already reviewed this place")

        try:
            review = facade.create_review(review_data)
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
    @jwt_required()
    def put(self, review_id):
        """Update an existing review."""

        review = facade.get_review(review_id)

        if not review:
            api.abort(404, "Review not found")

        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        if not is_admin and review.user.id != current_user_id:
            api.abort(403, "Unauthorized action")

        try:
            facade.update_review(review_id, api.payload)
            return facade.get_review(review_id), 200

        except (ValueError, KeyError) as error:
            api.abort(400, str(error))

    @api.response(204, "Review deleted")
    @jwt_required()
    def delete(self, review_id):
        """Delete a review."""

        review = facade.get_review(review_id)

        if not review:
            api.abort(404, "Review not found")

        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        if not is_admin and review.user.id != current_user_id:
            api.abort(403, "Unauthorized action")

        try:
            facade.delete_review(review_id)
            return "", 204

        except KeyError as error:
            api.abort(404, str(error))
