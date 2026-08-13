from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("users", description="User operations")

user_model = api.model(
    "User",
    {
        "id": fields.String(
            readOnly=True,
            description="The unique identifier of the user"
        ),
        "first_name": fields.String(
            required=True,
            description="First name of the user"
        ),
        "last_name": fields.String(
            required=True,
            description="Last name of the user"
        ),
        "email": fields.String(
            required=True,
            description="Email address of the user"
        ),
    },
)

user_create_model = api.model(
    "UserCreate",
    {
        "first_name": fields.String(
            required=True,
            description="First name of the user"
        ),
        "last_name": fields.String(
            required=True,
            description="Last name of the user"
        ),
        "email": fields.String(
            required=True,
            description="Email address of the user"
        ),
        "password": fields.String(
            required=True,
            description="User password"
        ),
    },
)

user_update_model = api.model(
    "UserUpdate",
    {
        "first_name": fields.String(
            description="First name of the user"
        ),
        "last_name": fields.String(
            description="Last name of the user"
        ),
        "email": fields.String(
            description="Email (Admin only)"
        ),
        "password": fields.String(
            description="Password (Admin only)"
        ),
    },
)


@api.route("/")
class UserList(Resource):

    @api.marshal_list_with(user_model)
    def get(self):
        """Retrieve the list of all users."""
        return facade.get_users(), 200

    @api.expect(user_create_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Register a new user."""

        user_data = api.payload

        required_fields = [
            "first_name",
            "last_name",
            "email",
            "password"
        ]

        for field in required_fields:
            if field not in user_data:
                api.abort(400, f"Missing required field: {field}")

        existing_user = facade.get_user_by_email(
            user_data["email"]
        )

        if existing_user:
            api.abort(400, "Email already registered")

        try:
            new_user = facade.create_user(user_data)
            return new_user, 201

        except ValueError as error:
            api.abort(400, str(error))


@api.route("/<string:user_id>")
@api.response(404, "User not found")
class UserResource(Resource):

    @api.marshal_with(user_model)
    def get(self, user_id):
        """Get user details by ID."""

        user = facade.get_user(user_id)

        if not user:
            api.abort(404, "User not found")

        return user, 200

    @api.expect(user_update_model)
    @api.marshal_with(user_model)
    @jwt_required()
    def put(self, user_id):
        """Update user information."""

        user = facade.get_user(user_id)

        if not user:
            api.abort(404, "User not found")

        current_user = get_jwt()
        is_admin = current_user.get("is_admin", False)
        token_user_id = get_jwt_identity()

        if not is_admin and token_user_id != user_id:
            api.abort(403, "Unauthorized action")

        update_data = api.payload.copy()

        if not is_admin:
            update_data.pop("email", None)
            update_data.pop("password", None)

        else:
            email = update_data.get("email")

            if email:
                existing_user = facade.get_user_by_email(email)

                if existing_user and existing_user.id != user_id:
                    api.abort(400, "Email already in use")

        try:
            facade.update_user(user_id, update_data)
            return facade.get_user(user_id), 200

        except ValueError as error:
            api.abort(400, str(error))
