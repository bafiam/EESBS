#the data transfer object (DTO) will be responsible for carrying data between processes
from flask_restplus import Namespace, fields


class SigninDTO:
    user_api = Namespace('user registration', description='user registration related operations')
    user = user_api.model('user registration', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        're_password': fields.String(required=True, description='re-enter user password'),
        
    })

class LoginDTO:
    login_api= Namespace('user login', description='user login related operations')
    user=login_api.model('user login', {
        'username': fields.String(required=True, description='The user username'),
        'password': fields.String(required=True, description='The user password'),
        
    })
class LogoutDTO:
    login_api= Namespace('user logout', description='user logout related operations')

class PassrestDTO:
    rest_api= Namespace('password reset', description='user password reset related operations')
    user=rest_api.model('password reset', {
        'old_password': fields.String(required=True, description='Old password'),
        'new_password': fields.String(required=True, description='New password'),
        
    })