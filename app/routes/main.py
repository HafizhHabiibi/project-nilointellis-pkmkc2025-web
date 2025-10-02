from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from app.controller.user_controller import UserController
from app.utils.auth_utils import web_session_required


# Create blueprint
main_bp = Blueprint('main', __name__)

# Initialize controller
user_controller = UserController()

# WEB ROUTES
@main_bp.route('/', methods=['GET', 'POST'])
def index():
    """login page"""
    if request.method == 'POST':
        result = user_controller.web_login(request)
        if result['success']:
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash(result['message'], 'error')

    return render_template('login.html')

@main_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """Web logout"""
    user_controller.logout()
    flash('Logout berhasil!', 'success')
    return redirect(url_for('main.index'))


