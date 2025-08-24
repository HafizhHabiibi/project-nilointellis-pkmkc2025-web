from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from app.controller.user_controller import UserController
from app.utils.auth_utils import web_session_required
from app.utils.lstm_utils import fetch_last_data, predict_future

# Create blueprint
prediksi_bp = Blueprint('prediksi', __name__)

# protected web session required
@prediksi_bp.route('/prediksi')
@web_session_required
def prediksi():
    """Prediksi page"""
    return render_template('prediksi.html')


@prediksi_bp.route("/run_prediksi", methods=["POST"])
@web_session_required
def run_prediksi():
    try:
        # Ambil data terakhir
        df = fetch_last_data()
        # Lakukan prediksi
        df_pred = predict_future(df)

        # Konversi ke JSON
        result = {
            "status": "success",
            "data": {
                "timestamps": df_pred.index.strftime("%Y-%m-%d %H:%M").tolist(),
                "ph": df_pred["ph"].round(2).tolist(),
                "suhu": df_pred["suhu"].round(2).tolist(),
                "turbidity": df_pred["turbidity"].round(2).tolist(),
                "tds": df_pred["tds"].round(2).tolist(),
            }
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })
