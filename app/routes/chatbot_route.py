from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from app.controller.user_controller import UserController
from app.utils.auth_utils import web_session_required

# Create blueprint
chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/chatbot')
@web_session_required
def chatbot():
    """Chatbot page"""
    return render_template('chatbot.html')

# route function chatbot disini