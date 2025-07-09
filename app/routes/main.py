from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

# Create blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """dasboard page"""
    return render_template('index.html')

# @main_bp.route('/dashboard')
# @login_required
# def dashboard():
#     """Dashboard page - requires login"""
#     return render_template('dashboard.html', user=current_user)

# @main_bp.route('/about')
# def about():
#     """About page"""
#     return render_template('about.html')
