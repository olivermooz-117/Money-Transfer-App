def test_register_creates_user_and_wallet(client):
    res = client.post(
        "/api/auth/register",
        json={"full_name": "Alice", "email": "alice@test.com", "password": "Password123!"},
    )
    assert res.status_code == 201
    body = res.get_json()
    assert body["user"]["email"] == "alice@test.com"
    assert body["user"]["wallet"]["balance"] == 0
    assert "token" in body


def test_register_rejects_duplicate_email(client):
    payload = {"full_name": "Alice", "email": "alice@test.com", "password": "Password123!"}
    client.post("/api/auth/register", json=payload)
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 409


def test_login_rejects_wrong_password(client):
    client.post(
        "/api/auth/register",
        json={"full_name": "Alice", "email": "alice@test.com", "password": "Password123!"},
    )
    res = client.post(
        "/api/auth/login", json={"email": "alice@test.com", "password": "WrongPass"}
    )
    assert res.status_code == 401
