from flask import request, jsonify, session
from app.models.user_model import get_user_login
from app.utils.auth_utils import generate_session_id

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
            # bikin session
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            session['session_id'] = generate_session_id()


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
        session.clear()

    def check_session(self):
        """Check apakah user sudah login"""
        return 'user_id' in session