from backend.app import app


def test_home_endpoint():
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.json["message"] == "AI Text-to-Image Generator API is running!"


def test_history_endpoint():
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/api/history")

    assert response.status_code == 200
    assert isinstance(response.json, list)