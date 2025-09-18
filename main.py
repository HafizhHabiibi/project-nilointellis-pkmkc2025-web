# AKAN DIABAIKAN KETIKA PRODUCTION
from app import app
from config import Config
from app.utils.scheduler import start_scheduler   # import scheduler untuk deteksi 

if __name__ == '__main__':
    print(f"Starting NiloIntellis Application...")
    print(f"URL: http://{Config.HOST}:{Config.PORT}")
    print(f"Debug Mode: {Config.DEBUG}")
    print(f"Database: {Config.MONGODB_URI}")

    # Aktifkan scheduler sebelum run server
    start_scheduler()

    # start_scheduler(app) akan jalan sekali ketika server Flask start.
    # Scheduler akan memanggil pipeline YOLOv8+DeepSORT setiap 5 menit.
    # Tidak mengganggu livestream realtime kamu.


    # app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
    app.run(host=Config.HOST, port=Config.PORT, debug=False, use_reloader=False)
