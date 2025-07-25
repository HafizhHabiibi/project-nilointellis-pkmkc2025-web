from flask import Flask, session, request
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Set permanent session lifetime dari config
app.permanent_session_lifetime = Config.PERMANENT_SESSION_LIFETIME

# Middleware untuk auto-refresh session pada request ke protected pages
@app.before_request
def refresh_session_on_activity():
    """Auto refresh session activity pada setiap request ke protected pages"""
    protected_paths = ['/dashboard', '/monitoring', '/prediksi', '/chatbot']
    
    # Check if current request is to a protected page
    if any(request.path.startswith(path) for path in protected_paths):
        # Check if user has active session
        if 'user_id' in session and 'username' in session:
            # Update last activity timestamp
            session['last_activity'] = datetime.utcnow().isoformat()
            session.permanent = True

# Import models and routes after app initialization
from app import models
from app.routes.main import main_bp

# Register blueprints
app.register_blueprint(main_bp)