# tests/conftest.py

import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from app.main import app  # Ensure this imports your FastAPI app
from app.db.database import get_database
from unittest.mock import patch
from app.core.security import create_access_token
from datetime import timedelta
from app.schemas.users import UserCreate
import os
from dotenv import load_dotenv

load_dotenv()

# Define test database URI and name
TEST_MONGODB_URI = os.getenv("TEST_MONGODB_URI", "mongodb://localhost:27017")
TEST_MONGODB_DB_NAME = os.getenv("TEST_MONGODB_DB_NAME", "test_bazzy_ecommerce")


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the session."""
    import asyncio
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_db():
    """Connect to the test MongoDB database."""
    client = AsyncIOMotorClient(TEST_MONGODB_URI)
    db = client[TEST_MONGODB_DB_NAME]
    yield db
    # Teardown: Drop the test database after tests
    await client.drop_database(TEST_MONGODB_DB_NAME)
    client.close()


@pytest.fixture
def override_get_database(test_db):
    """Override the get_database dependency to use the test database."""
    return test_db


@pytest.fixture
async def client(override_get_database):
    """Create an instance of the AsyncClient with overridden dependencies."""
    async def override_db():
        return override_get_database

    with patch("app.db.database.get_database", new=override_db):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac


@pytest.fixture
async def admin_token(test_db):
    """Create an admin user and return a valid JWT token for authentication."""
    # Create an admin user
    admin_user = {
        "username": "admin",
        "email": "admin@test.com",
        "password": "adminpassword",
        "role": "admin",
        "age": 35,
        "gender": "Male",
        "address": "Admin Address",
        "marital_status": "Married"
    }

    # Insert admin user into the test database
    user = await test_db["users"].find_one({"username": admin_user["username"]})
    if not user:
        from app.services.users import UserService
        from app.schemas.users import UserCreate

        user_create = UserCreate(**admin_user)
        await UserService.create_user(test_db, user_create)

    # Generate JWT token for admin user
    access_token = create_access_token(
        data={"sub": admin_user["username"]},
        expires_delta=timedelta(minutes=30)
    )
    return access_token
