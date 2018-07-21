from functools import wraps
from auth import auth

def authenticated(func):
    func.requires_authentication = True
    
    return func

def authorized(permissions=[]):
    def decorator(func):
        func.requires_authentication = True
        func.permissions = permissions
        return func

    return decorator