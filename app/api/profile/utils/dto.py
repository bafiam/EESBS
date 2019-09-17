#the data transfer object (DTO) will be responsible for carrying data between processes
from flask_restplus import Namespace, fields


class ProfileDTO:
    profile_api = Namespace('User profile', description='  User profile related operations')
    profile = profile_api.model('User profile', {
        'name': fields.String(required=True, description='user full name'),
        'location': fields.String(required=True, description='user location'),
        'phone': fields.String(required=True, description='user phone'),
        'till': fields.String(required=True, description='user till if any'),
        'about_me': fields.String(required=True, description='Say something about you'),
        
    })
class ConvertToServiceProviderDTO:
    #dto for user becoming a service provider
    BeServiceProvider=ProfileDTO.profile_api
    conv_profile =BeServiceProvider.model('Become a User service provider', {
        'be_service_provider': fields.String(required=True,description='Yes or No to become a service provvider'),
        'company_name': fields.String(required=True, description='user company'),
        
    })
