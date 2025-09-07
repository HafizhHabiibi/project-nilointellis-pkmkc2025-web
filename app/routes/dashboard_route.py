from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from app.controller.sensor_controller import SensorController, SensorData
from app.utils.auth_utils import web_session_required
from app.utils.ai_utils import get_ai_response
from app.utils.prompt_utils import ai_recommendation_prompt, ai_analysis_prompt
from config import Config

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

# Route to get AI recommendation based on latest sensor data
@dashboard_bp.route('/dashboard/get-ai-recommendation', methods=['POST'])
@web_session_required
def get_ai_recommendation():
    try:
        # Ambil data sensor terakhir
        sensor_controller = SensorController()
        latest_data = sensor_controller.get_realtime()
        
        if not latest_data:
            return jsonify({
                'status': 'error',
                'message': 'No sensor data available'
            }), 404

        # Bangun prompt
        prompt = ai_recommendation_prompt(latest_data)

        # Panggil AI
        recommendation = get_ai_response(
            api_key=Config.AI_RECOMMENDED_API_KEY,
            model_name="gemini-2.5-flash",
            prompt=prompt
        )
        
        return jsonify({
            'status': 'success',
            'recommendation': str(recommendation)
        }), 200

    except Exception as e:
        print(f"Error getting AI recommendation: {e}")
        return jsonify({
            'status': 'error',
            'message': 'AI sedang mengalami masalah, silakan coba lagi nanti.'
        }), 500

@dashboard_bp.route('/dashboard/get-ai-analyst-chart', methods=['POST'])
@web_session_required
def get_ai_analyst_chart():
    try:
        request_data = request.get_json()
        
        if not request_data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided'
            }), 400
        
        # Ambil statistik yang sudah dihitung di frontend
        statistics = request_data.get('statistics', {})
        filter_info = request_data.get('filter_info', {})
        raw_data = request_data.get('raw_data', [])
        
        if not statistics or not raw_data:
            return jsonify({
                'status': 'error',
                'message': 'No statistics data available for analysis'
            }), 404
        
        # Bangun prompt untuk analisis AI
        prompt = ai_analysis_prompt(statistics, filter_info, len(raw_data))
        
        # Panggil AI untuk analisis
        analysis = get_ai_response(
            api_key=Config.AI_RECOMMENDED_API_KEY,
            model_name="gemini-2.5-flash",
            prompt=prompt,
            temperature=0.3
        )
        
        return jsonify({
            'status': 'success',
            'analysis': str(analysis)
        }), 200
        
    except Exception as e:
        print(f"Error getting AI analysis: {e}")
        return jsonify({
            'status': 'error',
            'message': 'AI sedang mengalami masalah, silakan coba lagi nanti.'
        }), 500