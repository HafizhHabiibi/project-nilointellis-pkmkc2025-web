from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import asyncio

# === import pipeline deteksi ===
from app.utils.fish_death_pipeline import run_pipeline as run_fish_death_pipeline
from app.utils.fish_sick_pipeline import run_pipeline as run_fish_sick_pipeline  
# ↑ bikin file fish_sick_pipeline.py mirip pipeline ikan mati, 
# tapi logika fokus pada analisis gerakan/kelainan

scheduler = BackgroundScheduler()

def start_scheduler(app):
    with app.app_context():
        # === JOB 1: Deteksi ikan mati ===
        scheduler.add_job(
            lambda: asyncio.run(run_fish_death_pipeline()),
            trigger='interval',
            minutes=20,       # ⏱ interval 5 menit untuk ikan mati
            id='fish_death_job',
            replace_existing=True
        )

        # === JOB 2: Deteksi ikan sakit ===
        scheduler.add_job(
            lambda: asyncio.run(run_fish_sick_pipeline()),
            trigger='interval',
            minutes=30,      # ⏱ interval 10 menit untuk ikan sakit
            next_run_time=datetime.now() + timedelta(minutes=2),  
            # ↑ offset otomatis 2 menit setelah server start
            id='fish_sick_job',
            replace_existing=True
        )

        scheduler.start()
        print("[Scheduler] Monitoring ikan aktif ✅")
