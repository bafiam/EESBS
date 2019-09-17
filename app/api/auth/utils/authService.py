from appConfig import db
import uuid
import datetime
from app.api.auth.models import User
from app.api.auth.utils.validations import (validate_email_format, validate_empty_data, 
validate_password_format, validate_password_reset_format,
 validate_username_format, validate_empty_data_login)
from app.api.auth.utils.validations import encode_auth_token, decode_auth_token
from app.api.auth.models import BlacklistToken
from flask import g, request
# save a new user who registers


def register_new_user(data):
    # data validations
    #validate empty fields
    resp_validate_empty_data =validate_empty_data(data)
    if resp_validate_empty_data is not None:
        response_object = {
                'status': 'fail',
                'message': resp_validate_empty_data
            }
        return response_object, 202

    #validate email format fields
    resp_validate_email_format =validate_email_format(data)
    if resp_validate_email_format is not None:
        response_object = {
                'status': 'fail',
                'message': resp_validate_email_format
            }
        return response_object, 202

    #validate password format fields
    resp_validate_password_format=validate_password_format(data)
    if resp_validate_password_format is not None:
        response_object = {
                'status': 'fail',
                'message': resp_validate_password_format
            }
        return response_object, 202

    #validate username format fields
    resp_validate_username_format=validate_username_format(data)
    if resp_validate_username_format is not None:
        response_object = {
                'status': 'fail',
                'message': resp_validate_username_format
            }
        return response_object, 202
    #validate both passwords the same
    if data['password'] != data['re_password']:
        response_object = {
                'status': 'fail',
                'message': 'The passwords dont match'
            }
        return response_object, 202

    # go through the user table and returns only the first result or None if there are no results
    # only results specific to our query, ensure no other email exist
    user_email = User.query.filter_by(email=data['email']).first()
    # Also ensure no username duplication
    user_name = User.query.filter_by(email=data['username']).first()
    if not (user_email or user_name):
        new_user = User(
            # act as user indentifier rather than using the user_id/genereted
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
        # save the data
        save_changes(new_user)

        response_object = {
            'status': 'success',
            'message': 'User Successfully registered.'
        }
        return response_object, 201

    response_object = {
        'status': 'fail',
        'message': 'Username or Email already exists. Please Log in.',
    }
    return response_object, 202

    
# get all the users in the database
# return as a list

def get_all_users():
    return User.query.all()

#login user
def login_user(data):
    #validate the user login data
    #validate empty fields
    resp_validate_empty_data =validate_empty_data_login(data)
    if resp_validate_empty_data is not None:
        response_object = {
                'status': 'fail',
                'message': resp_validate_empty_data
            }
        return response_object, 202
    user = User.query.filter_by(username=data.get('username')).first()
    if not user:
        response_object = {
                    'status': 'fail',
                    'message': 'email or password does not match.'}
        return response_object, 202

    if not user.check_password(data.get('password')):
        response_object = {
                    'status': 'fail',
                    'message': 'email or password does not match.'}
        return response_object, 202
    auth_token = encode_auth_token(user.id)
    if auth_token:
        response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'Authorization': auth_token.decode()
                    }
        return response_object, 201
    response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
    return response_object, 500
    
    
# save the data in the database/data persist


def save_changes(data):
    db.session.add(data)
    db.session.commit()
    

def password_rest(data):
    resp_validate_pass_data=validate_password_reset_format(data)
    if resp_validate_pass_data:
        response_object = {
            'status': 'fail',
            'message': resp_validate_pass_data
            }
        return response_object, 202
    verify_old_pass =User.query.filter_by(username=g.token.get('username')).first()
    if not verify_old_pass.check_password(data.get('old_password')):
        response_object = {
                    'status': 'fail',
                    'message': 'The old password does not match.'}
        return response_object, 202
    passwrd=verify_old_pass.password=data['new_password']
    save_change=db.session.commit()
    if save_changes:
        response_object = {
            'status': 'success',
            'message': 'Password Successfully update.'
        }
        return response_object, 201
    response_object = {
            'status': 'fail',
            'message': 'Password update failed.'
        }
    return response_object, 202
    


    



