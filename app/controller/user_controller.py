from flask import request, jsonify, session
from app.models.user_model import get_user_login
from app.utils.auth_utils import create_user_session, clear_session, check_session, is_session_expired, refresh_session_activity

class UserController:
    """Controller authentication"""

    def web_login(self, request):
        """Handle login dari web form"""
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return {
                'success': False,
                'message': 'Username dan password harus diisi!'
            }

        user = get_user_login(username, password)

        if user:
            # Create session menggunakan helper function
            create_user_session(user)
            return {
                'success': True,
                'message': 'Login berhasil!'
            }
        else:
            return {
                'success': False,
                'message': 'Username atau password salah!'
            }

    def logout(self):
        """Handle logout"""
        clear_session()