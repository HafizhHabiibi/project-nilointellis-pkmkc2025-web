from .db import db
from datetime import datetime, timedelta

class SensorModel:
  def __init__(self):
    self.sensor_collection = db['sensor']

  def get_sensor_data(self):
    return list(self.sensor_collection.find())

  def get_sensor_data_real_time(self):
    return self.sensor_collection.find_one(sort=[('timestamp', -1)])

  def get_sensor_data_last_10_minutes(self):
    now = datetime.utcnow()
    ten_minutes_ago = now - timedelta(minutes=10)
    return list(self.sensor_collection.find({'timestamp': {'$gte': ten_minutes_ago, '$lte': now}}))

  def get_sensor_data_last_hour(self):
    now = datetime.utcnow()
    one_hour_ago = now - timedelta(hours=1)
    return list(self.sensor_collection.find({'timestamp': {'$gte': one_hour_ago, '$lte': now}}))

  def get_sensor_data_last_6_hours(self):
    now = datetime.utcnow()
    six_hours_ago = now - timedelta(hours=6)
    return list(self.sensor_collection.find({'timestamp': {'$gte': six_hours_ago, '$lte': now}}))

  def get_sensor_data_last_12_hours(self):
    now = datetime.utcnow()
    twelve_hours_ago = now - timedelta(hours=12)
    return list(self.sensor_collection.find({'timestamp': {'$gte': twelve_hours_ago, '$lte': now}}))

  def get_sensor_data_last_day(self):
    now = datetime.utcnow()
    one_day_ago = now - timedelta(days=1)
    return list(self.sensor_collection.find({'timestamp': {'$gte': one_day_ago, '$lte': now}}))
