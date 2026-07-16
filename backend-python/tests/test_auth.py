def test_login_success(client):

    client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
    )


    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )


    assert response.status_code == 200


    data = response.json()


    assert "access_token" in data

    assert data["token_type"] == "bearer"



def test_login_wrong_password(client):

    client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
    )


    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "wrongpassword"
        }
    )


    assert response.status_code == 401



def test_login_unknown_user(client):

    response = client.post(
        "/auth/login",
        json={
            "email": "missing@example.com",
            "password": "password123"
        }
    )


    assert response.status_code == 401

   
def test_get_current_user(client):

    client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
    )


    login_response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )


    token = login_response.json()["access_token"]


    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


    assert response.status_code == 200


    data = response.json()


    assert data["email"] == "test@example.com"

    assert data["username"] == "testuser" 