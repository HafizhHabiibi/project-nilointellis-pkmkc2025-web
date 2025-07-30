from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Import dan register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app

# Create app instance
app = create_app()