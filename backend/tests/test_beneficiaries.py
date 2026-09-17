def test_add_beneficiary(client, auth_headers):
    owner = auth_headers(email="owner@test.com")
    auth_headers(email="friend@test.com")  # must exist on platform

    res = client.post(
        "/api/beneficiaries",
        json={"name": "Friend", "account_email": "friend@test.com"},
        headers=owner,
    )
    assert res.status_code == 201
    body = res.get_json()
    assert body["name"] == "Friend"
    assert body["account_email"] == "friend@test.com"


def test_list_only_own_beneficiaries(client, auth_headers):
    owner = auth_headers(email="owner2@test.com")
    other = auth_headers(email="other2@test.com")
    auth_headers(email="friend2@test.com")

    client.post(
        "/api/beneficiaries",
        json={"name": "Friend", "account_email": "friend2@test.com"},
        headers=owner,
    )
    client.post(
        "/api/beneficiaries",
        json={"name": "Also Friend", "account_email": "friend2@test.com"},
        headers=other,
    )

    res = client.get("/api/beneficiaries", headers=owner)
    assert res.status_code == 200
    items = res.get_json()
    assert len(items) == 1
    assert items[0]["account_email"] == "friend2@test.com"


def test_cannot_add_self(client, auth_headers):
    headers = auth_headers(email="self@test.com")
    res = client.post(
        "/api/beneficiaries",
        json={"name": "Me", "account_email": "self@test.com"},
        headers=headers,
    )
    assert res.status_code == 400


def test_unknown_email_returns_404(client, auth_headers):
    headers = auth_headers(email="owner3@test.com")
    res = client.post(
        "/api/beneficiaries",
        json={"name": "Ghost", "account_email": "nobody@test.com"},
        headers=headers,
    )
    assert res.status_code == 404


def test_missing_fields_returns_400(client, auth_headers):
    headers = auth_headers(email="owner4@test.com")
    res = client.post(
        "/api/beneficiaries",
        json={"name": "Only Name"},
        headers=headers,
    )
    assert res.status_code == 400


def test_delete_own_beneficiary(client, auth_headers):
    owner = auth_headers(email="owner5@test.com")
    auth_headers(email="friend5@test.com")

    res = client.post(
        "/api/beneficiaries",
        json={"name": "Friend", "account_email": "friend5@test.com"},
        headers=owner,
    )
    beneficiary_id = res.get_json()["id"]

    res = client.delete(f"/api/beneficiaries/{beneficiary_id}", headers=owner)
    assert res.status_code == 200

    res = client.get("/api/beneficiaries", headers=owner)
    assert res.get_json() == []


def test_delete_other_users_beneficiary_returns_404(client, auth_headers):
    owner = auth_headers(email="owner6@test.com")
    other = auth_headers(email="other6@test.com")
    auth_headers(email="friend6@test.com")

    res = client.post(
        "/api/beneficiaries",
        json={"name": "Friend", "account_email": "friend6@test.com"},
        headers=owner,
    )
    beneficiary_id = res.get_json()["id"]

    res = client.delete(f"/api/beneficiaries/{beneficiary_id}", headers=other)
    assert res.status_code == 404