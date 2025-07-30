from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from app.controller.user_controller import UserController
from app.utils.auth_utils import web_session_required

# Create blueprint
prediksi_bp = Blueprint('prediksi', __name__)

# protected web session required
@prediksi_bp.route('/prediksi')
@web_session_required
def prediksi():
    """Prediksi page"""
    return render_template('prediksi.html')

# route function prediksi disini