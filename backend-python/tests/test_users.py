from app.crud.permission import (
    assign_permission_to_role,
    create_permission,
)


def test_create_user(client):

    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "Password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


def test_get_users(client):

    # Create test user
    create_response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "Password123"
        }
    )

    assert create_response.status_code == 200

    # Get the test database session
    from tests.conftest import TestingSessionLocal

    db = TestingSessionLocal()

    try:
        # Make the test user an admin
        from app.crud.user import get_user_by_email

        user = get_user_by_email(
            db,
            "test@example.com"
        )

        user.role = "admin"
        db.commit()

        # Create users.read permission
        permission = create_permission(
            db,
            "users.read",
            "Read users"
        )

        # Assign users.read to admin role
        assign_permission_to_role(
            db,
            "admin",
            permission.id
        )

    finally:
        db.close()

    # Log in as the admin user
    login_response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "Password123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Request users with authentication
    response = client.get(
        "/users/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    assert data[0]["username"] == "testuser"

    assert data[0]["email"] == "test@example.com"