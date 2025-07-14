from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

# Create blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
# @login_required
    """dasboard page"""
    return render_template('dashboard.html')

@main_bp.route('/monitoring')
def monitoring():
    """Monitoring page"""
    return render_template('monitoring.html')

@main_bp.route('/prediksi')
def prediksi():
    """Prediksi page"""
    return render_template('prediksi.html')
