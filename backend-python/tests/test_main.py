def test_root(client):
    unused_variable = "lint failure test"
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "API is running"
    }