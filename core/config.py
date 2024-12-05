"""
Core configuration for the application.

This module uses Pydantic's `BaseSettings` to manage environment variables 
and application configurations. It includes default values and loads additional 
settings from a `.env` file using `python-dotenv`.
"""

from pydantic import BaseSettings
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Application settings configuration.

    This class is used to define and validate the application's core settings.
    It leverages Pydantic's `BaseSettings` to manage environment variables.

    Attributes:
        MONGODB_URI (str): The MongoDB connection URI.
        MONGODB_DB_NAME (str): The name of the MongoDB database. Defaults to "edu_platform".
        SECRET_KEY (str): The secret key for securing the application. Defaults to "your_secret_key".
        ALGORITHM (str): The algorithm used for token signing. Defaults to "HS256".
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Token expiration time in minutes. Defaults to 30.
    """
    MONGODB_URI: str
    MONGODB_DB_NAME: str = "edu_platform"
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

# Instantiate the settings object
settings = Settings()
"""
Global settings object.

This is an instance of the `Settings` class that holds the application-wide configuration.
"""
