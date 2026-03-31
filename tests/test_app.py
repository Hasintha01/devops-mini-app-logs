from app import app


def test_home_endpoint():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Hello from DevOps on AWS" in response.data


def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert "s3_logging" in data


def test_users_endpoint():
    client = app.test_client()
    response = client.get("/users")

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 3
    assert data[0]["name"] == "Alice"


def test_test_log_endpoint():
    client = app.test_client()
    response = client.get("/test-log")

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Logs sent"
    assert "s3_enabled" in data