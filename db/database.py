"""
Database Connection Module.

This module manages the connection to the MongoDB database using Motor, an asynchronous MongoDB driver for Python.
It provides functions to connect to and disconnect from the database, as well as to retrieve the database instance.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# Global variables to hold the database client and instance
db_client = None
database = None


async def connect_db():
    """
    Establish a connection to the MongoDB database.

    Initializes the global `db_client` and `database` variables using the MongoDB URI and database name from settings.

    Raises:
        Exception: If the connection to MongoDB fails.
    """
    global db_client, database
    try:
        db_client = AsyncIOMotorClient(settings.MONGODB_URI)
        database = db_client[settings.MONGODB_DB_NAME]
        print("Connected to MongoDB")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise


async def close_db():
    """
    Close the connection to the MongoDB database.

    Closes the global `db_client` connection.

    Raises:
        Exception: If closing the connection fails.
    """
    try:
        db_client.close()
        print("Disconnected from MongoDB")
    except Exception as e:
        print(f"Failed to disconnect from MongoDB: {e}")
        raise


def get_database():
    """
    Retrieve the current MongoDB database instance.

    Returns:
        AsyncIOMotorDatabase: The MongoDB database instance.
    """
    return database


def get_db():
    """
    Alias for `get_database`.

    Returns:
        AsyncIOMotorDatabase: The MongoDB database instance.
    """
    return get_database()
