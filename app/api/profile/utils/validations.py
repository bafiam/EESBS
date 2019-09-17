import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
import re
def validate_tell_format(data):
    number = data['phone']
    # 2) Then contains 7 or 8 or 9. 
    # 3) Then contains 9 digits 
    rule = re.compile("[07-9][0-9]{9}") 
    if not rule.match(str(number)):
        return {'error': 'phone number must be of right format '}
    return None
 

def validate_tell_region(data):
    number = data['phone']
    verify=carrier._is_mobile(number_type(phonenumbers.parse(number, "KE")))
    if False:
        return {'error': 'phone number must be a valid international number'}
    return None

def validate_till(data):
    till=data['till']
    if till.isdigit() != True:
        return {'error': 'till number must be a interger'}
    return None   
    
def convert_into_bool(data):
    resp=data['be_service_provider']
    if resp == 'Yes':
        return True
    elif resp == 'No':
        return False      
    return {'error': 'Your input should be either Yes or No'}
    
