import re

def validate_username(username):
    return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

def validate_email(email):
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))

def validate_password(password):
    return len(password) >= 8