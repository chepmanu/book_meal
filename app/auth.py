from flask import request, jsonify, current_app

from functools import wraps

import jwt
import datetime
from .data import users

def get_user_by_email(email):
    for user in users:
        if user.email == email:
            return user

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message':'Token is missing!'}), 401
            
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            email = data['email']
            user = get_user_by_email(email)
            if not user:
                return jsonify({'message': 'Could not load  user'}), 401
            current_user = user
        
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated 



def generate_token(email):
    token = jwt.encode({'email': email, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, current_app.config['SECRET_KEY'])

    return token.decode('UTF-8')
