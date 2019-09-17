import datetime
import re
from appConfig import db
import jwt

from app.api.auth.models import BlacklistToken
# from app.api.auth.utils.authService import save_token
from config import SECRET_KEY as key


def validate_empty_data(validate_data):
    if not validate_data['email']:
        return {'error': 'Email required.', }
    if not validate_data['username']:
        return {'error': 'Username required.', }
    if not validate_data['username']:
        return {'error': 'password required.', }
    return None
def validate_empty_data_login(validate_data):
    if not validate_data['username']:
        return {'error': 'Username required.', }
    if not validate_data['username']:
        return {'error': 'password required.', }
    return None


def validate_email_format(validate_email):
    if not re.match(r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)", validate_email['email']):
        return {'error': 'Provide a valid email address'}
    return None


def validate_password_format(validate_password):
    if len(validate_password['password']) < 7:
        return {'error': 'Password must be at least 8 characters long!'}
    elif re.search('[0-9]', (validate_password['password'])) is None:
        return {'error': 'Password must have at least one number in it!'}
    elif re.search('[A-Z]', (validate_password['password'])) is None:
        return {'error': 'Password must have at least one capital letter in it!'}
    elif re.search('[a-z]', (validate_password['password'])) is None:
        return {'error': 'Password must have at least one alphabet letter in it!'}
    elif re.search('[!,#,$,%,&,*,+,-,<,=,>,?,@,^,_,{,|,},~,]', (validate_password['password'])) is None:
        return {'error': 'Password must have at least a special character in it!'}
    return None


def validate_username_format(validate_username):
    if not re.match("^[A-Za-z0-9_-]*$", validate_username['username']):
        return {'error': ' Username can only contains letters, numbers, underscores and dashes'}
    return None


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=80),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        auth_encoded = jwt.encode(
            payload,
            key,
            algorithm='HS256'
        )
        auth_encoded = jwt.encode(
            payload,
            key,
            algorithm='HS256'
        )
        return auth_encoded
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, key)
        is_blacklisted_token = BlacklistToken.query.filter_by(
            token=str(auth_token)).first()
        if is_blacklisted_token:
            return 'Token blacklisted. Please log in again.'
        else:
            return payload['sub']
    except jwt.ExpiredSignatureError:
        is_blacklisted_exp_token = BlacklistToken.query.filter_by(
            token=str(auth_token)).first()
        if not is_blacklisted_exp_token:
            blacklist_token = BlacklistToken(token=str(auth_token))
            db.session.add(blacklist_token)
            db.session.commit()
            return ' Signature expired. Please log in again.'
        return 'Token blacklisted. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def authenticate_active_token(active_token):
    auth_header = active_token
    if auth_header:  
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        resp = decode_auth_token(auth_token)
        # encode with an int soo if the resp is a string return false
        # factor in if not false == true
        if not isinstance(resp, str):
            blacklist_token = BlacklistToken(token=str(auth_token))
            db.session.add(blacklist_token)
            db.session.commit()
    
            return{
                'status': 'success',
                'message': 'Successfully logged out.'

            }, 201
        return{
            'status': 'failed',
            'message': resp
        }, 401
    return{
        'status': 'fail',
        'message': 'Provide a valid auth token.'
    }, 403

def validate_password_reset_format(validate_password):
    if len(validate_password['new_password']) < 7:
        return {'error': 'Password must be at least 8 characters long!'}
    elif re.search('[0-9]', (validate_password['new_password'])) is None:
        return {'error': 'Password must have at least one number in it!'}
    elif re.search('[a-z]', (validate_password['new_password'])) is None:
        return {'error': 'Password must have at least one alphabet letter in it!'}
    return None