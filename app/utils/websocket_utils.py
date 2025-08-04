from flask_socketio import emit, join_room, leave_room, disconnect
from flask import session
from app.utils.auth_utils import check_session

class WebSocketDashboard:
  def __init__(self, websocket, sensor_controller):
    self.websocket = websocket
    self.sensor_controller = sensor_controller
    self.register_events() # daftar cuy

  def register_events(self):
    @self.websocket.on('connect', namespace='/dashboard')
    def handle_connect():
      if not check_session():
        print("Client not authenticated")
        disconnect()
        return False

      print("Client connected to dashboard")
      join_room('dashboard_room')

      data_realtime = self.sensor_controller.realtime_update()
      if data_realtime:
        emit('sensor_update', {
          'type': 'realtime',
          'data': data_realtime
        })

    @self.websocket.on('disconnect', namespace='/dashboard')
    def handle_disconnect():
      print("Client disconnected from dashboard")
      leave_room('dashboard_room')
