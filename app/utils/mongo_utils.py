# # app/utils/mongo_utils.py
# import os
# from pymongo import MongoClient
# from pymongo.server_api import ServerApi
# from dotenv import load_dotenv
# from datetime import datetime
# import pytz

# load_dotenv()

# MONGO_URI = os.getenv("MONGODB_URI")
# MONGO_DB_NAME = os.getenv("DB_DATABASE", "nilo")
# MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME", "status_ikan")

# def get_mongo_client():
#     if not MONGO_URI:
#         raise RuntimeError("MONGODB_URI not set")
#     return MongoClient(MONGO_URI, server_api=ServerApi("1"))

# def save_result(status: str, details: dict = None):
#     """
#     Save a single result doc:
#       { status: "ada ikan mati" | "tidak ada ikan mati",
#         details: {...},      # optional additional info, counts etc
#         timestamp_wib: "YYYY-MM-DD HH:MM:SS"
#       }
#     """
#     client = get_mongo_client()
#     db = client[MONGO_DB_NAME]
#     coll = db[MONGO_COLLECTION_NAME]

#     # WIB timezone
#     tz = pytz.timezone("Asia/Jakarta")
#     ts_wib = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

#     doc = {
#         "status": status,
#         "details": details or {},
#         "timestamp_wib": ts_wib,
#         "ts_utc": datetime.utcnow()
#     }
#     coll.insert_one(doc)
#     client.close()
#     return doc

# def get_last_result():
#     client = get_mongo_client()
#     db = client[MONGO_DB_NAME]
#     coll = db[MONGO_COLLECTION_NAME]
#     doc = coll.find_one(sort=[("ts_utc", -1)])
#     client.close()
#     return doc
