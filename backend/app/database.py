from pymongo import MongoClient
from app.config import settings

def get_database():
    """Get MongoDB database connection"""
    client = MongoClient(settings.MONGO_URI)
    return client[settings.DATABASE_NAME]

def get_collection(collection_name):
    """Get a specific collection from the database"""
    db = get_database()
    return db[collection_name]

# Initialize database connection
db = get_database()
