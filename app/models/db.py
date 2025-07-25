from pymongo import MongoClient
from config import Config

try:
    # Create MongoDB connection using config
    client = MongoClient(Config.MONGODB_URI)
    db = client[Config.MONGODB_DATABASE]

    # Test connection
    client.admin.command('ping')
    print(f"✅ MongoDB connected successfully")
    # print(f"   Connection: {client.address}")
    # print(f"   Database: {Config.MONGODB_DATABASE}")
    # print(f"   Collections available: {db.list_collection_names()}")

except Exception as e:
    print(f"❌ MongoDB connection failed: {str(e)}")
    db = None