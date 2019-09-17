from appConfig import db
from flask import g
from app.api.profile.utils.validations import validate_tell_format, validate_tell_region,validate_till, convert_into_bool
from app.api.profile.models import UserProfile
from app.api.auth.models import User

def Become_Provider(data):
    resp_convert_into_bool=convert_into_bool(data)
    
    if resp_convert_into_bool is False:
        update_provider_false=User.query.filter_by(username=g.token.get('username')).update({
                User.is_provider :False
                })
        db.session.commit()
        response_object = {
                'status': 'success',
                'message': 'Your service provider privilege have been terminated.'
            }
        return response_object, 202
    elif resp_convert_into_bool is True:
        update_provider_true=User.query.filter_by(username=g.token.get('username')).update({
                User.is_provider:True
                })
        update_provider_comp_name=UserProfile.query.filter_by(user_id=g.token.get('pubic_id')).update({
        UserProfile.company_no:data['company_name']
        })
        db.session.commit()
        response_object = {
                        'status': 'success',
                        'message': 'You are now a service provider and the Company added.'} 
        return response_object, 201
    else:
        if resp_convert_into_bool is not (False or True):
            response_object = {
                'status': 'fail',
                'message': resp_convert_into_bool
            }
            return response_object, 202
    
   





def Update_profile(data):
    update_profile=UserProfile.query.filter_by(user_id=g.token.get('pubic_id')).first()
    if update_profile:
        resp_validate_tell_format =validate_tell_format(data)
        if  resp_validate_tell_format is not None:
            response_object = {
                'status': 'fail',
                'message': resp_validate_tell_format
            }
            return response_object, 202
        resp_validate_tell_region= validate_tell_region(data)
        if resp_validate_tell_region is not None:
            response_object = {
                'status': 'fail',
                'message': resp_validate_tell_region
            }
            return response_object, 202
        resp_validate_till=validate_till(data)
        if resp_validate_till is not None:
            response_object = {
                'status': 'failed',
                'message': resp_validate_till
            }
            return response_object, 202 
        update_profile=UserProfile.query.filter_by(user_id=g.token.get('pubic_id')).update({
            UserProfile.name :data['name'],
            UserProfile.location:data['location'],
            UserProfile.phone:data['phone'],
            UserProfile.till:data['till'],
            UserProfile.about_me:data['about_me']})
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Profile Successfully update.'} 
        return response_object, 201

    response_object = {
        'status': 'fail',
        'data': 'please add a profile first so as to view it '
    }
    return response_object, 202
                            


def Get_profile():
    get_profile=UserProfile.query.filter_by(user_id= g.token.get('pubic_id')).first()
    if get_profile:
        response_object = {
            'status': 'success',
            'resp': {
                            'name': get_profile.name,
                            'location': get_profile.location,
                            'email': get_profile.user.email,
                            'username': get_profile.user.username,
                            'company_no':get_profile.company_no,
                            'phone': get_profile.phone,
                            'till': get_profile.till,
                            'about_me': get_profile.about_me,
                            'provider':get_profile.user.is_provider
                            
                            }
        }
        return response_object, 201

    response_object = {
        'status': 'fail',
        'data': 'please add a profile first so as to view it '
    }
    return response_object, 202

    


def Add_profile(data):
    resp_validate_tell_format =validate_tell_format(data)
    if  resp_validate_tell_format is not None:
        response_object = {
                'status': 'fail',
                'message': resp_validate_tell_format
            }
        return response_object, 202
    resp_validate_tell_region= validate_tell_region(data)
    if resp_validate_tell_region is not None:
        response_object = {
                'status': 'fail',
                'message': resp_validate_tell_region
            }
        return response_object, 202
    add_profile=UserProfile(
        name=data['name'],
        location=data['location'],
        phone=int(data['phone']),
        till=int(data['till']),
        about_me=data['about_me'],
        user_id =g.token.get('pubic_id'))
    save = save_changes(add_profile)
    response_object = {
            'status': 'success',
            'message': 'Profile Successfully created.'
        }
    return response_object, 201

def save_changes(data):
    db.session.add(data)
    db.session.commit()
    

     


