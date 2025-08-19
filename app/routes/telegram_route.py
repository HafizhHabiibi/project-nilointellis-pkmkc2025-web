from flask import Blueprint, request, jsonify
from ..utils.telegram_utils import stop_chat, sokap

telegram_bp = Blueprint('telegram', __name__)

@telegram_bp.route("/telegram", methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        if text == "/start":
            sokap(chat_id)
        elif text == "/stop":
            stop_chat(chat_id)
    return jsonify({"ok": True})