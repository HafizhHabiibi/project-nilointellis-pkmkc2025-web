import pymongo
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config import Config
import tensorflow as tf
from pathlib import Path


# mongo connection
MONGO_URI = Config.MONGODB_URI
MONGO_DB_NAME = Config.MONGODB_DATABASE
MONGO_COLLECTION_NAME = Config.MONGODB_COLLECTION_SENSOR

# Load scaler & model -- AKAN DIPERBARUI NEXT TIME SETELAH MODEL VALID DENGAN DATA REAL

# 1. Dapatkan path absolut dari file skrip yang sedang berjalan (`.../app/utils/file.py`)
current_script_path = Path(__file__).resolve()

# 2. Dapatkan direktori 'app' dengan naik satu level dari direktori 'utils'
app_directory = current_script_path.parent.parent 

# 3. Bangun path yang benar ke folder model_ai dari direktori 'app'
scaler_path = app_directory / "model_ai" / "scaler.gz"
model_path = app_directory / "model_ai" / "lstm_model.keras"

# Load scaler & model dengan path yang sudah pasti benar
scaler = joblib.load(scaler_path)
model = tf.keras.models.load_model(model_path)

TIMESTEPS = 20 # PROJECT AKHIR DIGANTI MENJADI 60 , ARTINYA AKAN MENGGUNAKAN 60 MENIT ATAU 60 DATA TERAKHIR SEBAGAI INPUT KE MODEL UNTUK PREDIKSI 1 MENIT
N_FEATURES = 4
PRED_HORIZON = 120  # 120 menit = 2 jam

def get_mongo_client():
    return MongoClient(MONGO_URI, server_api=ServerApi('1'))

def fetch_last_data():
    client = None
    try:
        client = get_mongo_client()
        db = client[MONGO_DB_NAME]
        collection = db[MONGO_COLLECTION_NAME]

        # Ambil data 20 menit terakhir
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=TIMESTEPS) #MENGAMBIL DATA TERAKHIR SESUAI JUMLAH TIMESTEPS

        cursor = collection.find(
            {"timestamp": {"$gte": start_time, "$lte": end_time}},
            {"_id": 0, "timestamp": 1, "ph": 1, "suhu": 1, "turbidity": 1, "tds": 1}
        ).sort("timestamp", pymongo.ASCENDING)

        data_list = list(cursor)

        if len(data_list) < TIMESTEPS // 2:  # batas minimal 50%
            raise ValueError(
                f"Data hanya {len(data_list)} titik dalam 20 menit terakhir"
            )

        # Urutkan + resample ke 1 menit
        df = pd.DataFrame(data_list).sort_values("timestamp", ascending=True)
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True).dt.tz_convert("Asia/Jakarta")

        """
        resample digunakan jika ada lebih dari 1 data dalam 1 menit, dan interpolasi jika ada data yang kosong pada menit tertentu (mrngisi data yang kosong)
        .mean() digunakan kalau dalam satu menit ada beberapa data → ambil rata-rata.
        Hasilnya: setiap baris pasti mewakili 1 menit (meskipun tidak ada data asli di menit itu) --interpolasi.

        """
        df = df.set_index("timestamp").resample("1min").mean().interpolate()

        # Pastikan hasil akhir tetap pas 20 timesteps
        if len(df) < TIMESTEPS:
            raise ValueError("Hasil resampling tidak mencapai 20 timestep penuh.")

        return df.tail(TIMESTEPS)

    finally:
        if client:
            client.close()


def predict_future(df):
    # Ambil hanya kolom fitur
    data_scaled = scaler.transform(df[["ph", "suhu", "turbidity", "tds"]].values)

    input_seq = data_scaled[-TIMESTEPS:].reshape(1, TIMESTEPS, N_FEATURES)
    predictions = []

    for i in range(PRED_HORIZON):
        pred = model.predict(input_seq, verbose=0)
        predictions.append(pred[0])

        # Update input_seq: buang paling awal, tambahkan prediksi baru
        input_seq = np.append(input_seq[:,1:,:], [[pred[0]]], axis=1)

    # Invers transform hasil prediksi
    predictions = scaler.inverse_transform(predictions)

    # Buat DataFrame prediksi
    future_time_index = pd.date_range(
        start=df.index[-1] + timedelta(minutes=1),
        periods=PRED_HORIZON,
        freq="1min"
    )

    df_pred = pd.DataFrame(
        predictions,
        columns=["ph", "suhu", "turbidity", "tds"],
        index=future_time_index
    )

    return df_pred