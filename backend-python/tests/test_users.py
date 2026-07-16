def test_create_user(client):

    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

def test_get_users(client):

    client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
    )


    response = client.get("/users/")


    assert response.status_code == 200


    data = response.json()


    assert len(data) == 1

    assert data[0]["username"] == "testuser"

    assert data[0]["email"] == "test@example.com"