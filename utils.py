def validate_registration_data(data):
    errors = []
    if not data.get('full_name'):
        errors.append('Full name is required.')
    if not data.get('email'):
        errors.append('Email is required.')
    if not data.get('phone_number'):
        errors.append('Phone number is required.')
    if not data.get('location'):
        errors.append('Location is required.')
    if not data.get('password'):
        errors.append('Password is required.')
    if data.get('password') != data.get('confirm_password'):
        errors.append('Passwords do not match.')
    return errors

def validate_login_data(data):
    errors = []
    if not data.get('email'):
        errors.append('Email is required.')
    if not data.get('password'):
        errors.append('Password is required.')
    return errors
