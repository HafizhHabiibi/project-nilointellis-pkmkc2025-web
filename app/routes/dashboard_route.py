from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from app.controller.sensor_controller import SensorController, SensorData
from app.utils.auth_utils import web_session_required

# Create blueprint
dashboard_bp = Blueprint('dashboard', __name__)

# protected web session required
@dashboard_bp.route('/dashboard')
@web_session_required
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')

# route function dashboard disini
@dashboard_bp.route('/dashboard/filter', methods=['POST', 'GET'])
@web_session_required
def filter_dashboard():
    try:
        sensor_controller = SensorData()
        tanggalAwal = request.form.get('tanggal_awal')
        tanggalAkhir = request.form.get('tanggal_akhir')
        granulitas = request.form.get('granulitas')

        data = sensor_controller.get_data_ringkasan(tanggalAwal, tanggalAkhir, granulitas)

        if data and not isinstance(data, dict) or not data.get('error'):
            return jsonify({
                'status': 'success',
                'data': data,
                'tanggalAwal': tanggalAwal,
                'tanggalAkhir': tanggalAkhir,
                'granulitas': granulitas
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'No data found'
            }), 404

    except Exception as e:
        print(f"Error getting sensor data: {e}")
        return jsonify({'error': 'Failed to get sensor data'}), 500
