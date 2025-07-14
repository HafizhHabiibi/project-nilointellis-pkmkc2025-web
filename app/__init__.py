from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app,db)

# Import models and routes after app initialization
from app import models
from app.routes.main import main_bp

# Register blueprints
app.register_blueprint(main_bp)