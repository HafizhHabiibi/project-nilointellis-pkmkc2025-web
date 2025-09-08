from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from app.controller.user_controller import UserController
from app.utils.auth_utils import web_session_required
from config import Config
import os

# Create blueprint
monitoring_bp = Blueprint('monitoring', __name__)

@monitoring_bp.route('/monitoring')
@web_session_required
def monitoring():
    # ambil ws_url dari config, atau set default
    wss_url = os.getenv('NILOCAM_WSS_URL', 'wss://nilocam.my.id')
    return render_template('monitoring.html', ws_url=wss_url)
