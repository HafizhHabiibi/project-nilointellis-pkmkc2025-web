from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Set permanent session lifetime dari config
app.permanent_session_lifetime = Config.PERMANENT_SESSION_LIFETIME

# Import models and routes after app initialization
from app import models
from app.routes.main import main_bp

# Register blueprints
app.register_blueprint(main_bp)