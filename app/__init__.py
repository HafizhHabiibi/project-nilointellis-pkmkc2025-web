from flask import Flask
from config import Config
from flask_socketio import SocketIO
from app.utils.websocket_utils import WebSocketDashboard
from app.controller.sensor_controller import SensorController

from app.routes import main_bp
from app.routes.dashboard_route import dashboard_bp
from app.routes.prediksi_route import prediksi_bp
from app.routes.monitoring_route import monitoring_bp
from app.routes.chatbot_route import chatbot_bp
from app.routes.telegram_route import telegram_bp
from app.routes.sensor_route import sensor_bp

# tambahan scheduer untuk computer vision
from app.utils.scheduler import start_scheduler 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    websocket = SocketIO(app, cors_allowed_origins="*")

    # register __init__ controller
    sensor_controller = SensorController(websocket)

    # register init utils
    WebSocketDashboard(websocket, sensor_controller)

    # Import dan register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(prediksi_bp)
    app.register_blueprint(monitoring_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(telegram_bp)
    app.register_blueprint(sensor_bp)

    # aktifkan scheduler setelah semua siap
    start_scheduler(app)

    return app, websocket

# Create app instance
app, websocket = create_app()