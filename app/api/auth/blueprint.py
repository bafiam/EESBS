# Import flask dependencies

from flask import Blueprint
from flask_restplus import Api, Resource

from app.api.auth import views
from app.api.auth.views import api_sign, api_login, api_logout, api_reset
from app.api.auth.views import authorizations
# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

api = Api(mod_auth, version='1.0',title='Event Equipment and Service Booking System',
description='A documentation for the Event Equipment and Service Booking System User Authentication module', authorizations=authorizations )

# #add endpoint when using conventinal api testing
# from app.api.auth.views import UserSignin
# api.add_resource(UserSignin, '/register')

# #add endpoint when using swagger api testing
api.add_namespace(api_sign, path='/register')
api.add_namespace(api_login,path='/login')
api.add_namespace(api_logout,path='/logout')
api.add_namespace(api_reset,path='/password_reset')