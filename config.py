import os
from datetime import timedelta
from dotenv import load_dotenv

# Load .env
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Flask Core Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'janganlupa')
    DEBUG = os.environ.get('FLASK_DEBUG', '1').lower() in ['true', '1', 'yes']

    # Server Configuration
    HOST = os.environ.get('FLASK_HOST', '127.0.0.1')
    PORT = int(os.environ.get('FLASK_PORT', 5000))

    # MongoDB Configuration

    # connection mongo
    MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb+srv://nilointellis123:RisangKarbit123@cluster0.t6t6amy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

    # db mongo
    MONGODB_DATABASE = os.environ.get('DB_DATABASE', 'nilointellis')

    # Session Timeout - otomatis expire setelah 1 jam tidak aktif
    SESSION_TIMEOUT_HOURS = int(os.environ.get('SESSION_TIMEOUT_HOURS', 1))
    PERMANENT_SESSION_LIFETIME = timedelta(hours=SESSION_TIMEOUT_HOURS)