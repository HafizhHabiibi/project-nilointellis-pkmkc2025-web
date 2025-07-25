from functools import wraps
from flask import request, jsonify, session
import uuid

# Session controller

def generate_session_id():
    """Generate session ID sederhana"""
    return str(uuid.uuid4())

def session_required(f):
    """Decorator untuk memerlukan session pada endpoint"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': 'Session tidak ditemukan, silakan login'
            }), 401

        current_user = {
            'user_id': session['user_id'],
            'username': session['username']
        }

        return f(current_user, *args, **kwargs)

    return decorated
