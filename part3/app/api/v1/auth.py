from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade


api = Namespace('auth', description='Authentication operations')


login_model = api.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})


@api.route('/login')
class Login(Resource):

    @api.expect(login_model)
    def post(self):

        data = api.payload

        user = facade.get_user_by_email(data['email'])

        if not user:
            api.abort(401, "Invalid email or password")

        if not user.verify_password(data['password']):
            api.abort(401, "Invalid email or password")

        token = create_access_token(
            identity=user.id,
            additional_claims={
                "is_admin": user.is_admin
            }
        )

        return {
            "access_token": token
        }, 200
