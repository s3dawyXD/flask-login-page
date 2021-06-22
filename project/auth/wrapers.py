from flask import Flask, request, abort, jsonify, redirect
from functools import wraps
from .jwt_api import JWT_API


'''
helping functions
'''
def get_token_auth_header():
    if 'Authorization' not in request.headers:
        abort(401)
    
    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')

    if len(header_parts) != 2:
        abort(401)
    elif header_parts[0].lower() != 'bearer':
        abort(401)

    return header_parts[1]

'''
@wraping functions
'''
def require_auth(f):
    @wraps(f)
    def wraper(*args,**kwargs):
        jwt = get_token_auth_header()
        cl = JWT_API()
        try:
            payload = cl.verify_decode_jwt(jwt)
        except:
            abort(401)
        return f(payload, *args, **kwargs)
    return wraper

def check_auth(f):
    @wraps(f)
    def wraper(*args, **kwargs):
        jwt = get_token_auth_header()
        cl = JWT_API()
        if jwt == 'null':
            msg = {'jwt':'first visit!'}
        else:
            if cl.check_jwt_exp(jwt):
                msg = {'jwt':'go and update your jwt'}
            else:
                msg = {'jwt':'you are good to go'}
        
        return f(msg, *args, **kwargs)
    return wraper