def test_add_funds_increases_balance(client, auth_headers):
    headers = auth_headers()
    res = client.post("/api/wallet/add-funds", json={"amount": 500}, headers=headers)
    assert res.status_code == 201
    assert res.get_json()["wallet"]["balance"] == 500

    res = client.get("/api/wallet", headers=headers)
    assert res.get_json()["wallet"]["balance"] == 500
    assert res.get_json()["analytics"]["total_received"] == 500


def test_add_funds_rejects_non_positive_amount(client, auth_headers):
    headers = auth_headers()
    res = client.post("/api/wallet/add-funds", json={"amount": 0}, headers=headers)
    assert res.status_code == 400
