import os
from datetime import timedelta
from dotenv import load_dotenv

# Load .env
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Flask Core Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = os.environ.get('FLASK_DEBUG').lower() in ['true', '1', 'yes']

    # Server Configuration
    HOST = os.environ.get('FLASK_HOST')
    PORT = int(os.environ.get('FLASK_PORT'))

    # MongoDB Configuration

    # connection mongo
    MONGODB_URI = os.environ.get('MONGODB_URI')

    # db mongo
    MONGODB_DATABASE = os.environ.get('DB_DATABASE')
    
    # collection mongo
    MONGO_COLLECTION_MONITORING = os.getenv("MONGO_COLLECTION_MONITORING")
    MONGO_COLLECTION_MONITORING_HEALTH = os.getenv("MONGO_COLLECTION_MONITORING_HEALTH")
    MONGODB_COLLECTION_SENSOR = os.getenv("MONGODB_COLLECTION_SENSOR")
    MONGODB_COLLECTION_CHAT_ID = os.getenv("MONGODB_COLLECTION_CHAT_ID")

    # Session Timeout - otomatis expire setelah 1 jam tidak aktif
    SESSION_TIMEOUT_HOURS = int(os.environ.get('SESSION_TIMEOUT_HOURS', 1))
    PERMANENT_SESSION_LIFETIME = timedelta(hours=SESSION_TIMEOUT_HOURS)

    # Telegram Token
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    
    # AI Configuration
    AI_RECOMMENDED_API_KEY= os.environ.get('AI_RECOMMENDED_API_KEY')
    CHART_ANALYST_AI_API_KEY = os.environ.get('CHART_ANALYST_AI_API_KEY')
    DEATH_ANALYST_AI_API_KEY = os.environ.get('DEATH_ANALYST_AI_API_KEY')
    CHATBOT_API_KEY = os.environ.get('CHATBOT_API_KEY')
    
    # Nilocam WebSocket URL
    NILOCAM_WSS_URL = os.getenv('NILOCAM_WSS_URL')
    
    # YOLO Model Path
    MODEL_PATH = os.getenv("YOLO_MODEL_PATH")