from flask import Blueprint, render_template, jsonify, session, request
from app.utils.auth_utils import web_session_required
from app.utils.storage_anaylisis_utils import load_analysis, save_analysis
from app.utils.prompt_utils import death_analysis_prompt
from app.utils.ai_utils import get_ai_response
from app.utils.sensor_utils import hitung_statistik
from app.controller.sensor_controller import SensorData
from config import Config
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi


monitoring_bp = Blueprint('monitoring', __name__)

MONGO_URI = Config.MONGODB_URI
MONGO_DB_NAME = Config.MONGODB_DATABASE
MONGO_COLLECTION_NAME = Config.MONGO_COLLECTION_MONITORING
MONGO_COLLECTION_HEALTH = Config.MONGO_COLLECTION_MONITORING_HEALTH

def get_mongo_client():
    return MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

# ---------- PAGE ----------
@monitoring_bp.route('/monitoring')
@web_session_required
def monitoring():
    wss_url = Config.NILOCAM_WSS_URL
    return render_template('monitoring.html', ws_url=wss_url)

# ---------- API: IKAN MATI ----------
@monitoring_bp.route('/api/monitoring/status')
def get_latest_status():
    client = get_mongo_client()
    db = client[MONGO_DB_NAME]
    collection = db[MONGO_COLLECTION_NAME]
    latest = collection.find_one(sort=[('_id', -1)])
    if not latest:
        return jsonify({"status": "belum ada data", "timestamp": None})
    return jsonify({"status": latest.get('status'), "timestamp": latest.get('timestamp')})

# ---------- API: IKAN SAKIT ----------
@monitoring_bp.route('/api/monitoring/health')
def get_latest_health():
    client = get_mongo_client()
    db = client[MONGO_DB_NAME]
    collection = db[MONGO_COLLECTION_HEALTH]
    latest = collection.find_one(sort=[('_id', -1)])
    if not latest:
        return jsonify({"count_sick": 0, "timestamp": None})
    return jsonify({"count_sick": latest.get('count_sick', 0), "timestamp": latest.get('timestamp')})

# ---------- API: Analisis Kematian Ikan ----------
@monitoring_bp.route('/monitoring/get-death-analysis', methods=['POST'])
def get_death_analysis():
    try:
        data = request.get_json()
        status = data.get("status", "tidak ada ikan mati")
        timestamp = data.get("timestamp")
        
        # # Ambil data sensor 24 jam terakhir
        # sensor_controller = SensorData()
        # sensor_data, sensor_count = sensor_controller.get_data_24_jam_terakhir()
        
        # data dummy untuk simulasi
        sensor_data = [
            {'suhu': 28.5, 'ph': 7.2, 'tds': 300, 'turbidity': 5, 'timestamp': '2025-09-30T07:00:00Z'},
            {'suhu': 29.0, 'ph': 7.0, 'tds': 320, 'turbidity': 6, 'timestamp': '2025-09-30T07:10:00Z'},
            {'suhu': 30.0, 'ph': 6.8, 'tds': 350, 'turbidity': 7, 'timestamp': '2025-09-30T07:20:00Z'},
            {'suhu': 30.0, 'ph': 6.8, 'tds': 350, 'turbidity': 7, 'timestamp': '2025-09-30T07:20:00Z'},
            {'suhu': 40.0, 'ph': 12.8, 'tds': 950, 'turbidity': 1000, 'timestamp': '2025-09-30T07:20:00Z'},
        ]
        sensor_count = len(sensor_data)
        
        # Validasi data sensor
        if not sensor_data or (isinstance(sensor_data, dict) and sensor_data.get('error')):
            return jsonify({
                'status': 'error',
                'message': 'No data found'
            }), 404    

        # kalau status bukan "ada ikan mati" → reset session
        if status.lower() != "ada ikan mati":
            return jsonify({
                "status": "success",
                "analysis": ""
            }), 200

        # Menghitung statistik data sensor
        stats = hitung_statistik(sensor_data)
        
        # load cache
        cache = load_analysis()

        # cek apakah sudah ada analisis terbaru
        if (status in cache) and (timestamp <= cache[status]["timestamp"]):
            death_analysis = cache[status]
        else:
            # Bangun prompt
            prompt = death_analysis_prompt(stats, sensor_count, granulitas="10 menit")
            
            # Panggil AI
            analysis_text = get_ai_response(
                api_key=Config.AI_RECOMMENDED_API_KEY,
                model_name="gemini-2.5-flash",
                prompt=prompt,
                temperature=0.3
            )

            # update cache
            death_analysis = {
                "analysis": str(analysis_text),
                "timestamp": timestamp
            }
            
            cache[status] = death_analysis
            save_analysis(cache)

        return jsonify({
            "status": "success",
            "analysis": death_analysis.get("analysis"),
            "timestamp": death_analysis.get("timestamp")
        }), 200

    except Exception as e:
        print(f"Error get_death_analysis: {e}")
        return jsonify({
            "status": "error",
            "message": "AI sedang mengalami masalah, coba lagi nanti."
        }), 500
        
