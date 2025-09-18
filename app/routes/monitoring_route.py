from flask import Blueprint, render_template, jsonify
from app.utils.auth_utils import web_session_required
from config import Config
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi

monitoring_bp = Blueprint('monitoring', __name__)

MONGO_URI = os.getenv("MONGODB_URI")
MONGO_DB_NAME = os.getenv("DB_DATABASE", "nilo")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_MONITORING", "status_ikan")
MONGO_COLLECTION_HEALTH = os.getenv("MONGO_COLLECTION_MONITORING_HEALTH", "monitoring_health")

def get_mongo_client():
    return MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

# ---------- PAGE ----------
@monitoring_bp.route('/monitoring')
@web_session_required
def monitoring():
    wss_url = os.getenv('NILOCAM_WSS_URL', 'wss://nilocam.my.id')
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
