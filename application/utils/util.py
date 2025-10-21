from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify
import jwt

SECRET_KEY = "your_super_secret_mechanic_shop_key_change_this_in_production"

def encode_token(customer_id):
    """Generate a JWT token for a customer"""
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(hours=1),  # Expires in 1 hour
        'iat': datetime.now(timezone.utc),  # Issued at
        'sub': str(customer_id)  # Subject - customer ID (must be string)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def token_required(f):
    """Decorator to protect routes with token authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Look for token in Authorization header
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Token format invalid! Use: Bearer <token>'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Decode the token
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            customer_id = int(data['sub'])  # Get customer ID from token and convert to int
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        
        # Pass customer_id to the wrapped function
        return f(customer_id, *args, **kwargs)
    
    return decorated