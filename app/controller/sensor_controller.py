from flask import request, jsonify, session
from flask_socketio import emit
from app.models.sensor_model import SensorModel
import time
import threading
from datetime import datetime

class SensorController:
  def __init__(self, websocket):
    self.websocket = websocket
    self.sensor_model = SensorModel()
    self.is_running = False
    self.thread = None

  def realtime_update(self):
    if not self.is_running:
        self.is_running = True
        self.thread = threading.Thread(target=self._realtime_worker)
        self.thread.daemon = True
        self.thread.start()

  def get_realtime(self):
    try:
      data = self.sensor_model.get_sensor_data_real_time()
      if data:
        data['id'] = str(data['_id'])
        data['timestamp'] = data['timestamp'].isoformat()
        del data['_id']
        return data
      return None
    except Exception as e:
      print(f"Error getting real-time sensor data: {e}")
      return None


  def _realtime_worker(self):
    while self.is_running:
      try:
        # Get latest sensor data
        realtime_data = self.get_realtime()

        if realtime_data:
            # Emit to all connected clients
            self.websocket.emit('sensor_update', {
                'type': 'realtime',
                'data': realtime_data
            }, namespace='/dashboard')

        time.sleep(1)  # Update every 2 seconds

      except Exception as e:
          print(f"Error in realtime worker: {e}")
          time.sleep(5)