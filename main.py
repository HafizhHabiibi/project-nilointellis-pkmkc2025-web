from app import app
from config import Config

if __name__ == '__main__':
    print(f"Starting NiloIntellis Application...")
    print(f"URL: http://{Config.HOST}:{Config.PORT}")
    print(f"Debug Mode: {Config.DEBUG}")
    print(f"Database: {Config.MONGODB_URI}")
    print(f"Session Timeout: {Config.SESSION_TIMEOUT_HOURS} hour(s)")

    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)