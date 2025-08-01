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

    # Session Timeout - otomatis expire setelah 1 jam tidak aktif
    SESSION_TIMEOUT_HOURS = int(os.environ.get('SESSION_TIMEOUT_HOURS', 1))
    PERMANENT_SESSION_LIFETIME = timedelta(hours=SESSION_TIMEOUT_HOURS)