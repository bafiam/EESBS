from flask import request
from flask_restplus import Resource
from app.api.profile.utils.dto import ProfileDTO, ConvertToServiceProviderDTO
from app.api.auth.utils.decorators import jwt_token_required,jwt_token_required, jwt_provider_required
from app.api.profile.utils.profileService import Add_profile, Get_profile, Update_profile, Become_Provider
#dto for user registration
api_profile = ProfileDTO.profile_api
_profile = ProfileDTO.profile

# api_beprofile = ConvertToServiceProviderDTO.BeServiceProvider
_beprofile = ConvertToServiceProviderDTO.conv_profile

@api_profile.route('/')
@api_profile.response(202, 'The request has been accepted for processing, but the processing has not been completed.')
class UserSignin(Resource):
    @api_profile.response(201, 'Profile Successfully created.')
    @api_profile.doc('create user profile', security='apiKey')
    @api_profile.expect(_profile, validate=True)
    @api_profile.header('Authorization', 'JWT Token', required=True)
    @jwt_token_required
    def post(self):
        "Post user profile data"
        data = request.json
        return Add_profile(data=data)

    @api_profile.response(201, 'Profile Successfully Data Retrived .')
    @api_profile.doc('user profile data', security='apiKey')
    @api_profile.header('Authorization', 'JWT Token', required=True)
    @jwt_token_required
    def get(self):
        "Get user profile data"
        
        return Get_profile()

    @api_profile.response(201, 'Profile Successfully updated.')
    @api_profile.doc('Edit user profile', security='apiKey')
    @api_profile.expect(_profile, validate=True)
    @api_profile.header('Authorization', 'JWT Token', required=True)
    @jwt_token_required
    def patch(self):
        "Update user profile data"
        data = request.json
        return Update_profile(data=data)

    @api_profile.response(201, 'Profile Successfully updated to a provider.')
    @api_profile.doc('Edit user role to provider', security='apiKey')
    @api_profile.expect(_beprofile, validate=True)
    @api_profile.header('Authorization', 'JWT Token', required=True)
    @jwt_token_required
    def put(self):
        "Update user profile data to a provider"
        data = request.json
        return Become_Provider(data=data)