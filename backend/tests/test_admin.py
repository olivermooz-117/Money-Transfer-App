def test_non_admin_forbidden_on_users(client, auth_headers):
    headers = auth_headers(email="normal@test.com")
    res = client.get("/api/admin/users", headers=headers)
    assert res.status_code == 403


def test_non_admin_forbidden_on_analytics(client, auth_headers):
    headers = auth_headers(email="normal2@test.com")
    res = client.get("/api/admin/analytics", headers=headers)
    assert res.status_code == 403


def test_admin_lists_users(client, admin_headers, auth_headers):
    auth_headers(email="member@test.com")
    headers = admin_headers(email="admin1@test.com")

    res = client.get("/api/admin/users", headers=headers)
    assert res.status_code == 200
    users = res.get_json()
    emails = {u["email"] for u in users}
    assert "admin1@test.com" in emails
    assert "member@test.com" in emails


def test_admin_analytics_shape(client, admin_headers, auth_headers):
    headers = admin_headers(email="admin2@test.com")
    # create some activity
    user = auth_headers(email="payer@test.com")
    client.post("/api/wallet/add-funds", json={"amount": 100}, headers=user)

    res = client.get("/api/admin/analytics", headers=headers)
    assert res.status_code == 200
    body = res.get_json()
    assert "total_users" in body
    assert "total_wallet_balance" in body
    assert "total_transfer_volume" in body
    assert "total_fees_collected" in body
    assert body["total_users"] >= 2


def test_admin_profit_trends(client, admin_headers):
    headers = admin_headers(email="admin3@test.com")
    res = client.get("/api/admin/profit-trends", headers=headers)
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)


def test_admin_lists_transactions(client, admin_headers, auth_headers):
    headers = admin_headers(email="admin4@test.com")
    res = client.get("/api/admin/transactions", headers=headers)
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)


def test_admin_update_user(client, admin_headers, auth_headers, app):
    auth_headers(email="target@test.com")
    headers = admin_headers(email="admin5@test.com")

    # find target id
    users = client.get("/api/admin/users", headers=headers).get_json()
    target = next(u for u in users if u["email"] == "target@test.com")

    res = client.put(
        f"/api/admin/users/{target['id']}",
        json={"full_name": "Updated Name", "is_active": False},
        headers=headers,
    )
    assert res.status_code == 200
    body = res.get_json()
    assert body["full_name"] == "Updated Name"
    assert body["is_active"] is False