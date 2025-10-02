import cv2
import numpy as np
import datetime
from pathlib import Path
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from config import Config
import websockets
import asyncio
from app.utils.telegram_utils import send_notif


# mongo connection
MONGO_URI = Config.MONGODB_URI
MONGO_DB_NAME = Config.MONGODB_DATABASE
MONGO_COLLECTION_NAME = Config.MONGODB_COLLECTION_MONITORING

WS_URL = Config.NILOCAM_WSS_URL
MODEL_PATH = Config.MODEL_PATH

# Load YOLOv8
yolo_model = YOLO(MODEL_PATH)

def get_mongo_client():
    # return MongoClient(MONGO_URI, server_api=ServerApi('1'))
    return MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

def save_status_to_mongo(status: str):
    """Simpan hasil analisis ke MongoDB"""
    client = get_mongo_client()
    db = client[MONGO_DB_NAME]
    collection = db[MONGO_COLLECTION_NAME]

    now_wib = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    doc = {
        "status": status,
        "timestamp": now_wib.strftime("%Y-%m-%d %H:%M:%S")
    }
    collection.insert_one(doc)

async def capture_frames(n=3):
    """Ambil n frame dari WebSocket kamera"""
    frames = []
    try:
        async with websockets.connect(WS_URL) as ws:
            for _ in range(n):
                frame_bytes = await ws.recv()
                frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
                frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
                if frame is not None:
                    frames.append(frame)
    except Exception as e:
        print("WS capture error:", e)
    return frames

def run_yolo_on_frames(frames):
    """Cek apakah ada ikan mati di salah satu frame"""
    for frame in frames:
        results = yolo_model(frame)
        for r in results:
            boxes = r.boxes
            if boxes is not None and len(boxes) > 0:
                for cls_id in boxes.cls.tolist():
                    if int(cls_id) == 1:  # kelas 1 = ikan_mati
                        return True
    return False

def run_deepsort_validation():
    """Tracking selama 30 detik, cek centroid movement"""
    tracker = DeepSort(max_age=30)
    cap = cv2.VideoCapture(WS_URL)  # fallback RTSP jika ada
    start = datetime.datetime.now()
    centroids = {}

    while (datetime.datetime.now() - start).seconds < 30:
        ret, frame = cap.read()
        if not ret:
            break
        results = yolo_model(frame)
        detections = []
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                detections.append(([x1, y1, x2 - x1, y2 - y1], conf, cls_id))
        tracks = tracker.update_tracks(detections, frame=frame)
        for t in tracks:
            if not t.is_confirmed():
                continue
            tid = t.track_id
            x1, y1, x2, y2 = t.to_ltrb()
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            if tid not in centroids:
                centroids[tid] = []
            centroids[tid].append((cx, cy))

    cap.release()

    # Hitung movement
    for tid, points in centroids.items():
        if len(points) < 2:
            continue
        x_mov = max(p[0] for p in points) - min(p[0] for p in points)
        y_mov = max(p[1] for p in points) - min(p[1] for p in points)
        if x_mov < 10 and y_mov < 10:  # threshold px
            return True
    return False

async def run_pipeline():
    print("[Pipeline] Mulai jalan...")
    frames = await capture_frames(3)
    print(f"[Pipeline] Jumlah frame tertangkap: {len(frames)}")

    if not frames:
        print("[Pipeline] Tidak ada frame")
        save_status_to_mongo("tidak ada data")
        return

    detected_dead = run_yolo_on_frames(frames)
    print(f"[Pipeline] YOLO mendeteksi ikan mati? {detected_dead}")

    if not detected_dead:
        save_status_to_mongo("tidak ada ikan mati")
        return

    confirmed_dead = run_deepsort_validation() #melanjutkan dengan analisis deepsort 
    print(f"[Pipeline] DeepSORT validasi hasil: {confirmed_dead}")

    if confirmed_dead: #jika setelah analisis dengan deepsort tervalidasi ada yang mati , maka menjalankan...
        save_status_to_mongo("ada ikan mati")
        # TAMBAHKAN PEMANGGILAN FUNGSI UNTUK NOTIF KE TELEGRAM DI SINI 
        pesan = "*ada ikan mati woii!! coba dicek , kalo scam maaf yaa, masih prototipe hehe..*"
        send_notif(pesan)

        # TAMBAHKAN PEMANGGILAN FUNGSI UNTUK ANALISIS IKAN MATI DENGAN GEN AI DI SINI


    else:
        save_status_to_mongo("tidak ada ikan mati")
