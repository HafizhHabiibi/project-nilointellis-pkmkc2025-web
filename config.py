import os
from datetime import timedelta
from dotenv import load_dotenv

# Load .env
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configuration for NiloIntellis Application"""

    # Flask Core Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'janganlupa')
    DEBUG = os.environ.get('FLASK_DEBUG', '1').lower() in ['true', '1', 'yes']

    # Server Configuration
    HOST = os.environ.get('FLASK_HOST', '127.0.0.1')
    PORT = int(os.environ.get('FLASK_PORT', 5000))

    # MongoDB Configuration

    # connection mongo
    MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/nilointellis')

    # db mongo
    MONGODB_DATABASE = os.environ.get('DB_DATABASE', 'nilointellis')

    # Session Configuration
    SESSION_PERMANENT = True
    SESSION_TYPE = os.environ.get('SESSION_TYPE', 'filesystem')
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False  # Set True jika menggunakan HTTPS

    # Session Timeout - otomatis expire setelah 1 jam tidak aktif
    SESSION_TIMEOUT_HOURS = int(os.environ.get('SESSION_TIMEOUT_HOURS', 1))
    PERMANENT_SESSION_LIFETIME = timedelta(hours=SESSION_TIMEOUT_HOURS)