import requests
from flask import current_app
from pymongo import MongoClient
from datetime import datetime
from config import Config


# MongoDB setup
MONGO_URI = Config.MONGODB_URI
MONGO_DB_NAME = Config.MONGODB_DATABASE
MONGO_DB_COLLECTION_CHAT_ID = Config.MONGODB_COLLECTION_CHAT_ID

TELEGRAM_BOT_TOKEN = Config.TELEGRAM_BOT_TOKEN

def get_db():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    return client[MONGO_DB_NAME]

def save_chat_id(chat_id):
    db = get_db()
    collection = db[MONGO_DB_COLLECTION_CHAT_ID]
    if not collection.find_one({"chat_id":chat_id}):
        collection.insert_one({
            "chat_id": chat_id,
            "joined_at": datetime.utcnow()
        })

def delete_chat_id(chat_id):
    db = get_db()
    collection = db[MONGO_DB_COLLECTION_CHAT_ID]
    result = collection.delete_one({"chat_id": chat_id})
    if result.deleted_count > 0:
        print(f"Chat ID {chat_id} Berhasil Dihapus")
    else:
        print(f"Chat ID {chat_id} Tidak Ditemukan")

def get_chat_id():
    db = get_db()
    collection = db[MONGO_DB_COLLECTION_CHAT_ID]
    return [doc["chat_id"] for doc in collection.find()]

def send_notif(message):
    token = Config.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    chat_ids = get_chat_id()

    for chat_id in chat_ids:
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': "Markdown"
        }
        try:
            requests.post(url, data=payload)
        except Exception as e:
            print(f"Gagal kirim ke {chat_id}:", e)

def sokap(chat_id):
    """Respon ketika user memulai bot dengan /start."""
    save_chat_id(chat_id)
    pesan = (
        "*👋📡 Selamat datang di NiloIntellisBOT!*\n\n"
        "PKM-KC Universitas Teknologi Yogyakarta 2025"
    )
    token = Config.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        'chat_id': chat_id,
        'text': pesan,
        'parse_mode': "Markdown"
    }

    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Gagal kirim sambutan ke {chat_id}:", e)

def stop_chat(chat_id):
    delete_chat_id(chat_id)
    pesan = (
        "*❌ Notifikasi dari NiloIntellis Bot berhenti!* \n\n"
        "Ketik */start* untuk menerima notifikasi kembali!"
    )
    token = Config.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        'chat_id': chat_id,
        'text' : pesan,
        'parse_mode': "Markdown"
    }

    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Gagal kirim pesan stop ke {chat_id}:", e)