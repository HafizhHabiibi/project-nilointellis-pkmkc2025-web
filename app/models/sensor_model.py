from .db import db
from datetime import datetime, timedelta

class SensorModel:
  def __init__(self):
    self.sensor_collection = db['sensor']

  def get_sensor_data_real_time(self):
    return self.sensor_collection.find_one(sort=[('timestamp', -1)])

  def get_sensor_statistik(self, tanggal_awal, tanggal_akhir, granulitas):
    granulitas_mapping = {
      '1 menit': 1,
      '5 menit': 5,
      '10 menit': 10,
      '30 menit': 30,
      '1 jam': 60,
      '6 jam': 360,
      '12 jam': 720,
      'hari': 1440, #dalam menit
      'minggu': 10080,
      'bulan': 43200  # 30 hari
    }

    interval_menit = granulitas_mapping.get(granulitas)

    try:
      query = {
        'timestamp': {
          '$gte': tanggal_awal,
          '$lte': tanggal_akhir
        }
      }
      cursor = self.sensor_collection.find(query).sort('timestamp', 1)
      rentang_data = list(cursor)
      if not rentang_data:
        print("gada datanya cari apa?.")
        return []

      data_filter=[]
      start_time = rentang_data[0]['timestamp']

      for data in rentang_data[1:]:
        current_time = data['timestamp']
        time_diff = (current_time - start_time).total_seconds() / 60
        if time_diff >= interval_menit:
          data_filter.append(data)
          start_time = current_time

      return data_filter

    except Exception as e:
      print(f"Error getting sensor data: {e}")
      return []
