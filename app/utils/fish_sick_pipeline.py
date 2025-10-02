# app/utils/fish_sick_pipeline.py
import cv2
import time
import datetime
import numpy as np
import asyncio
import websockets
from config import Config
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from pymongo import MongoClient
from statistics import median


# mongo connection
MONGO_URI = Config.MONGODB_URI
MONGO_DB_NAME = Config.MONGODB_DATABASE
MONGO_COLLECTION_NAME = Config.MONGODB_COLLECTION_MONITORING_HEALTH

WS_URL = Config.NILOCAM_WSS_URL
MODEL_PATH = Config.MODEL_PATH

CAPTURE_DURATION = 30      # detik observasi
CAPTURE_FPS = 1            # fps sampling

# Threshold heuristik (bisa dikalibrasi)
SICK_MIN_DISP = 15
SICK_MAX_DISP = 80
IDLE_PIXEL_THRESH = 5
IDLE_RATIO_SICK = 0.3
REL_SPEED_FACTOR = 0.6

# -------------------------------
# Load YOLO + DeepSORT
# -------------------------------
yolo_model = YOLO(MODEL_PATH)
tracker = DeepSort(max_age=10)

# -------------------------------
# MongoDB client
# -------------------------------
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]

# -------------------------------
# Helper fungsi
# -------------------------------
def euclid(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def analyze_track(track_points, timestamps):
    """
    Analisis 1 ikan berdasarkan track centroid sepanjang durasi observasi.
    Return: "sick" / "healthy"
    """
    N = len(track_points)
    if N < 2:
        return "unknown"

    T = timestamps[-1] - timestamps[0]
    step_dists = [euclid(track_points[i], track_points[i-1]) for i in range(1, N)]
    L = sum(step_dists)
    idle_ratio = sum(1 for d in step_dists if d < IDLE_PIXEL_THRESH) / max(1, len(step_dists))

    # Rule: ikan sakit → gerak terbatas tapi tidak sepenuhnya mati
    if SICK_MIN_DISP <= L <= SICK_MAX_DISP and idle_ratio >= IDLE_RATIO_SICK:
        return "sick"

    return "healthy"

async def capture_frames_websocket(duration=CAPTURE_DURATION, fps=CAPTURE_FPS):
    """
    Capture frames dari websocket kamera (Raspberry Pi/Cloudflare).
    Return: list frame dalam interval tertentu.
    """
    frames = []
    start_time = time.time()
    try:
        async with websockets.connect(WS_URL) as ws:
            while time.time() - start_time < duration:
                try:
                    frame_bytes = await asyncio.wait_for(ws.recv(), timeout=5)
                    frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
                    frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
                    if frame is not None:
                        frames.append(frame)
                except Exception as e:
                    print("[FishSickPipeline] Frame capture error:", e)
                await asyncio.sleep(1 / fps)
    except Exception as e:
        print("[FishSickPipeline] WebSocket error:", e)
    return frames

# -------------------------------
# Main pipeline
# -------------------------------
async def run_pipeline():
    print("[FishSickPipeline] Mulai observasi...")

    # Ambil frame dari kamera via websocket
    frames = await capture_frames_websocket()
    if not frames:
        print("[FishSickPipeline] Tidak ada frame yang tertangkap")
        return None

    track_history = {}
    time_history = {}
    start_time = time.time()

    for frame in frames:
        results = yolo_model.predict(frame, imgsz=640, conf=0.25, verbose=False)
        detections = []
        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                if cls == 0:  # hanya analisis ikan hidup
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    detections.append(([x1, y1, x2-x1, y2-y1], conf, cls))

        # Update tracker
        tracks = tracker.update_tracks(detections, frame=frame)
        now = time.time()

        for t in tracks:
            if not t.is_confirmed():
                continue
            tid = t.track_id
            ltrb = t.to_ltrb()
            cx = int((ltrb[0] + ltrb[2]) / 2)
            cy = int((ltrb[1] + ltrb[3]) / 2)

            track_history.setdefault(tid, []).append((cx, cy))
            time_history.setdefault(tid, []).append(now - start_time)

    # -------------------------------
    # Analisis tiap track
    # -------------------------------
    statuses = []
    speeds = []

    for tid, points in track_history.items():
        ts = time_history[tid]
        status = analyze_track(points, ts)
        statuses.append(status)

        # simpan avg_speed untuk analisis group
        step_dists = [euclid(points[i], points[i-1]) for i in range(1, len(points))]
        L = sum(step_dists)
        T = ts[-1] - ts[0] if len(ts) > 1 else 1
        avg_speed = L / T
        speeds.append(avg_speed)

    # refine analisis sakit dengan perbandingan median speed
    if speeds:
        group_median = median(speeds)
        for i, (tid, points) in enumerate(track_history.items()):
            if statuses[i] == "healthy":
                step_dists = [euclid(points[j], points[j-1]) for j in range(1, len(points))]
                L = sum(step_dists)
                T = time_history[tid][-1] - time_history[tid][0] if len(time_history[tid]) > 1 else 1
                avg_speed = L / T
                if avg_speed < REL_SPEED_FACTOR * group_median:
                    statuses[i] = "sick"

    # sick_count = statuses.count("sick")

    # result = {
    #     "timestamp": datetime.datetime.utcnow() + datetime.timedelta(hours=7),
    #     "count_sick": sick_count
    # }
    # collection.insert_one(result)

    sick_count = statuses.count("sick")
    now_wib = datetime.datetime.utcnow() + datetime.timedelta(hours=7)

    result = {
        "timestamp": now_wib.strftime("%Y-%m-%d %H:%M:%S"),  # seragam dengan ikan mati
        "count_sick": sick_count
    }
    collection.insert_one(result)


    print(f"[FishSickPipeline] Selesai. Sakit={sick_count}")
    return result
