from flask import request
from flask_restplus import Resource
from app.api.auth.utils.authService import get_all_users, register_new_user, login_user, password_rest
from app.api.auth.utils.validations import authenticate_active_token
from app.api.auth.utils.dto import SigninDTO, LoginDTO, LogoutDTO, PassrestDTO
from app.api.auth.utils.decorators import jwt_token_required,jwt_token_required, jwt_provider_required

authorizations={
    'apiKey':{
        'type':'apiKey',
        'name':'Authorization',
        'in': 'header'

    }
}
#dto for user registration
api_sign = SigninDTO.user_api
_user = SigninDTO.user


@api_sign.route('/')
@api_sign.response(202, 'The request has been accepted for processing, but the processing has not been completed.')
class UserSignin(Resource):
    @api_sign.response(201, 'User successfully created.')
    @api_sign.doc('create a new user')
    @api_sign.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return register_new_user(data=data)

#dto for user login
api_login=LoginDTO.login_api
_userlogin=LoginDTO.user

@api_login.route('/')
@api_login.response(202, 'The request has been accepted for processing, but the processing has not been completed.')
class UserLogin(Resource):
    @api_login.response(201, 'Successfully logged in.')
    @api_login.doc('user login')
    @api_login.expect(_userlogin, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return login_user(post_data)

#dto for user logout
api_logout=LogoutDTO.login_api
@jwt_token_required
@api_logout.route('/')
class LogoutAPI(Resource):
    @api_logout.header('Authorization', 'JWT Token', required=True)
    @api_login.response(201, 'Successfully logged  out.')
    @api_logout.doc('logout a user', security='apikey')

    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        return authenticate_active_token(active_token=auth_header)

#dto for user password reset
api_reset=PassrestDTO.rest_api
_userlogin=PassrestDTO.user


@api_reset.route('/')
@api_reset.response(202, 'The request has been accepted for processing, but the processing has not been completed.')
class UserPassRest(Resource):
    @api_reset.response(201, 'Password Successfully update.')
    @api_reset.header('Authorization', 'JWT Token', required=True)
    @api_reset.doc('password reset',security='apiKey')
    @api_reset.expect(_userlogin, validate=True)
    @jwt_token_required
    def patch (self):
        # get the post data
        reset_data = request.json
        return password_rest(reset_data)