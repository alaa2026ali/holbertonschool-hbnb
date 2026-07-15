from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'id': fields.String(readOnly=True, description='The unique identifier of the user'),
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email address of the user')
})

user_create_model = api.model('UserCreate', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email address of the user'),
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email address of the user')
})


@api.route('/')
class UserList(Resource):

    @api.marshal_list_with(user_model)
    def get(self):
        """Retrieve the list of all users"""
        return facade.get_users(), 200

    @api.expect(user_create_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Register a new user"""
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            api.abort(400, "Email already registered")

        try:
            new_user = facade.create_user(user_data)
            return new_user, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<string:user_id>')
@api.response(404, 'User not found')
class UserResource(Resource):

    @api.marshal_with(user_model)
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")

        return user, 200

    @api.expect(user_update_model)
    @api.marshal_with(user_model)
    def put(self, user_id):
        """Update user information"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")

        try:
            facade.update_user(user_id, api.payload)
            return facade.get_user(user_id), 200
        except ValueError as e:
            api.abort(400, str(e))
