from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from app.controller.user_controller import UserController
from app.utils.auth_utils import web_session_required

# Create blueprint
monitoring_bp = Blueprint('monitoring', __name__)

# protected web session required
@monitoring_bp.route('/monitoring')
@web_session_required
def monitoring():
    """Monitoring page"""
    return render_template('monitoring.html')

# route function monitoring disini