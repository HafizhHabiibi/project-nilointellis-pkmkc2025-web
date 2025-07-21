from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

# Create blueprint
main_bp = Blueprint('main', __name__)

# PR : bikin sesion login buat semua page

@main_bp.route('/')
def index():
    """login page"""
    return render_template('login.html')

@main_bp.route('/dashboard')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')

@main_bp.route('/monitoring')
def monitoring():
    """Monitoring page"""
    return render_template('monitoring.html')

@main_bp.route('/prediksi')
def prediksi():
    """Prediksi page"""
    return render_template('prediksi.html')

@main_bp.route('/chatbot')
def chatbot():
    """Chatbot page"""
    return render_template('chatbot.html')


