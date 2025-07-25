from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_required, current_user
from app.controller.user_controller import UserController

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
            return redirect(url_for('main.dashboard'))
        else:
            flash(result['message'], 'error')

    return render_template('login.html')

@main_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """Web logout"""
    user_controller.logout()
    flash('Logout berhasil!', 'success')
    return redirect(url_for('main.index'))

# PROTECTED WEB ROUTES
@main_bp.route('/dashboard')
def dashboard():
    """Dashboard page"""
    if not user_controller.check_session():
        flash('Silakan login terlebih dahulu!', 'error')
        return redirect(url_for('main.index'))
    return render_template('dashboard.html')

@main_bp.route('/monitoring')
def monitoring():
    """Monitoring page"""
    if not user_controller.check_session():
        flash('Silakan login terlebih dahulu!', 'error')
        return redirect(url_for('main.index'))
    return render_template('monitoring.html')

@main_bp.route('/prediksi')
def prediksi():
    """Prediksi page"""
    if not user_controller.check_session():
        flash('Silakan login terlebih dahulu!', 'error')
        return redirect(url_for('main.index'))
    return render_template('prediksi.html')

@main_bp.route('/chatbot')
def chatbot():
    """Chatbot page"""
    if not user_controller.check_session():
        flash('Silakan login terlebih dahulu!', 'error')
        return redirect(url_for('main.index'))
    return render_template('chatbot.html')
