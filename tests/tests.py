# tests/test_users.py

import pytest
from app.schemas.users import UserCreate
from bson import ObjectId

@pytest.mark.asyncio
async def test_add_user(client, admin_token, test_db):
    """
    Test adding a new user.
    """
    # Define new user data
    new_user = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
        "role": "user",
        "age": 25,
        "gender": "Female",
        "address": "123 Test Street",
        "marital_status": "Single"
    }

    # Make POST request to add user
    response = await client.post(
        "/users/",
        json=new_user,
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    # Assert response status code
    assert response.status_code == 201, f"Unexpected status code: {response.status_code}"

    # Assert response data
    data = response.json()
    assert "id" in data
    assert data["username"] == new_user["username"]
    assert data["email"] == new_user["email"]
    assert data["role"] == new_user["role"]
    assert data["age"] == new_user["age"]
    assert data["gender"] == new_user["gender"]
    assert data["address"] == new_user["address"]
    assert data["marital_status"] == new_user["marital_status"]
    assert "wallet" in data
    assert data["wallet"]["balance"] == 0.0

    # Verify user is in the database
    user_in_db = await test_db["users"].find_one({"_id": ObjectId(data["id"])})
    assert user_in_db is not None, "User was not found in the database."
    assert user_in_db["username"] == new_user["username"]
    assert user_in_db["email"] == new_user["email"]
    assert user_in_db["role"] == new_user["role"]
    assert user_in_db["age"] == new_user["age"]
    assert user_in_db["gender"] == new_user["gender"]
    assert user_in_db["address"] == new_user["address"]
    assert user_in_db["marital_status"] == new_user["marital_status"]


@pytest.mark.asyncio
async def test_delete_user(client, admin_token, test_db):
    """
    Test deleting an existing user.
    """
    # First, create a user to delete
    user_to_delete = {
        "username": "deletetestuser",
        "email": "deletetestuser@example.com",
        "password": "deletepassword",
        "role": "user",
        "age": 30,
        "gender": "Male",
        "address": "456 Delete Street",
        "marital_status": "Married"
    }

    from app.services.users import UserService
    from app.schemas.users import UserCreate

    user_create = UserCreate(**user_to_delete)
    created_user = await UserService.create_user(test_db, user_create)
    user_id = created_user.id

    # Ensure user exists in the database
    user_in_db = await test_db["users"].find_one({"_id": ObjectId(user_id)})
    assert user_in_db is not None, "User to delete was not found in the database."

    # Make DELETE request to delete the user
    response = await client.delete(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    # Assert response status code
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Assert response data
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == user_to_delete["username"]
    assert data["email"] == user_to_delete["email"]
    assert data["role"] == user_to_delete["role"]

    # Verify user is deleted from the database
    deleted_user = await test_db["users"].find_one({"_id": ObjectId(user_id)})
    assert deleted_user is None, "User was not deleted from the database."

    # Verify associated wallet is also deleted
    wallet = await test_db["wallets"].find_one({"user_id": user_id})
    assert wallet is None, "Associated wallet was not deleted from the database."
