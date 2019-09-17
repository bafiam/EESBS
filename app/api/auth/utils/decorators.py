import token
from functools import wraps

from flask import g, request

from app.api.auth.models import User
from app.api.auth.utils.validations import decode_auth_token


def token_auth(new_request):
    """[jwt required decorator..custom made]
    
    *start bychecking if the header has an authorisation token
    *if true, then split the token and extract the one on index [1]..[sub]
    *now decode the [sub] to get the payload used to encode it
    *use isisntance to check the decoded results is of int type,
    coz we used the user_id from user table to encode
    *if its true, find the user represented by that user_id from db, 
    it will return either a user or none
    *when a user is returned, not None, check if the admin has approved that account, 
    to access the resouces.
    * if it is true,then we use flask.g module to store the, 
    user data into g.active_user
    * the rest are else handlers incase of error
        
    """
    if 'Authorization' in request.headers:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = decode_auth_token(auth_token)
            if isinstance(resp, int):
                user = User.query.filter_by(id=resp).first()
                if user:
                    response_object = {
                        'status': 'success',
                        'data': {
                            'user_id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'admin': user.is_admin,
                            'provider': user.is_provider,
                            'password': user.password_hash,
                            'pubic_id':user.public_id
                            }
                            }
                    return response_object, 200
                    
                else:
                    return{
                'status': '401',
                'message':'user does not exist,'
                            'invalid token'},400
            else:
                return {
                'status': '401',
                'message':resp
                },400
        
        return {
                    'status': '401',
                    'message':"invalid authorisation token!!, login again to get another"
                    },400
    else:
        return{
                'status': '401',
                'message':"Your request has no authorisation header!!,log in first"
            },401

def jwt_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = token_auth(request)
        token = data.get('data')

        if not token:
            return data, status
        g.token=token
        return f(*args, **kwargs)

    return decorated
def jwt_admin_required(f):
    
    @functools.wraps(f)
    def decorator_admin_token_auth(*args, **kwargs):
        data, status = token_auth(request)
        token = data.get('data')

        if not token:
            return data, status

        admin = token.get('admin')
        if admin is False:
            response_object = {
                'status': 'fail',
                'message': 'admin token required'
            }
            return response_object, 401
        g.token=token
        return f(*args, **kwargs)
     
    return decorator_admin_token_auth

def jwt_provider_required(f):
    
    @functools.wraps(f)
    def decorator_provider_token_auth(*args, **kwargs):
        data, status = token_auth(request)
        token = data.get('data')

        if not token:
            return data, status

        provider = token.get('provider')
        if provider is True:
            response_object = {
                'status': 'fail',
                'message': 'Service provider token required'
            }
            return response_object, 401
        g.token=token
        return f(*args, **kwargs)
     
    return decorator_provider_token_auth