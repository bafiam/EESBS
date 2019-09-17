# Import flask dependencies
from flask import Blueprint
from flask_restplus import Api, Resource

from app.api.profile import views
from app.api.auth.views import authorizations
from app.api.profile.views import api_profile
# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_profile = Blueprint('profile', __name__, url_prefix='/api/v1/profile')

api = Api(mod_profile, version='1.0',title='Event Equipment and Service Booking System',
description='A documentation for the Event Equipment and Service Booking System User profile',
 authorizations=authorizations )


# #add endpoint when using swagger api testing
api.add_namespace(api_profile, path='/profile')