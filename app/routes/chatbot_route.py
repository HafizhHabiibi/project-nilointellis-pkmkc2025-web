from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from config import Config
from app.controller.user_controller import UserController
from app.utils.auth_utils import web_session_required
from app.utils.prompt_utils import role_chatbot
from app.utils.ai_utils import get_ai_reply
from datetime import datetime


# Create blueprint
chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route("/chatbot", methods=["GET", "POST"])
@web_session_required
def chatbot():
    if "messages" not in session:
        session['chat'] = [role_chatbot()]
        session["messages"] = []

    if request.method == "POST":
        data = request.get_json()
        user_input = data.get("message", "").strip()
        
        if user_input:
            session['chat'].append({"role": "user", "content": user_input})
            session["messages"].append({
                "role": "user",
                "content": user_input,
                "time": datetime.now().strftime("%H:%M")
            })

            try: 
                # Get AI response
                ai_reply = get_ai_reply(
                    api_key=Config.CHATBOT_API_KEY,
                    model_name="GLM-4-Flash",
                    prompt=session['chat']
                )
                
                session["chat"].append({"role": "assistant", "content": ai_reply})
                session["messages"].append({
                    "role": "assistant",
                    "content": ai_reply,
                    "time": datetime.now().strftime("%H:%M")
                })

                session.modified = True
                
                return jsonify({
                    "status": "success",
                    "response": ai_reply,
                })
                
            except Exception as e:
                print(f"Error getting AI recommendation: {e}")
                return jsonify({
                    "status": "error",
                    "message": "Maaf, terjadi kesalahan. Silakan coba lagi."
                }), 500
        
        return jsonify({"status": "error", "message": "Pesan tidak boleh kosong."}), 400
    return render_template("chatbot.html", messages=session["messages"])