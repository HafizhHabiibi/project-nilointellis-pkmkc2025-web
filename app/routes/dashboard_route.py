from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from app.controller.sensor_controller import SensorController
from app.utils.auth_utils import web_session_required

# Create blueprint
dashboard_bp = Blueprint('dashboard', __name__)

# protected web session required
@dashboard_bp.route('/dashboard')
@web_session_required
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')

# route function dashboard disini