# app/db/database.py

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

db_client = None
database = None

async def connect_db():
    global db_client, database
    db_client = AsyncIOMotorClient(settings.MONGODB_URI)
    database = db_client[settings.MONGODB_DB_NAME]
    print("Connected to MongoDB")

async def close_db():
    db_client.close()
    print("Disconnected from MongoDB")

def get_database():
    return database

# Add this function
def get_db():
    return get_database()
