def test_send_money_charges_fee_and_moves_balance(client, auth_headers):
    sender_headers = auth_headers(email="sender@test.com")
    auth_headers(email="receiver@test.com")

    client.post("/api/wallet/add-funds", json={"amount": 1000}, headers=sender_headers)

    res = client.post(
        "/api/beneficiaries",
        json={"name": "Receiver", "account_email": "receiver@test.com"},
        headers=sender_headers,
    )
    beneficiary_id = res.get_json()["id"]

    res = client.post(
        "/api/transactions/send",
        json={"beneficiary_id": beneficiary_id, "amount": 200},
        headers=sender_headers,
    )
    assert res.status_code == 201
    body = res.get_json()
    assert body["transaction"]["fee"] == 2.0  # 1% of 200
    assert body["wallet"]["balance"] == 798.0  # 1000 - 200 - 2 fee


def test_send_money_rejects_insufficient_balance(client, auth_headers):
    sender_headers = auth_headers(email="sender2@test.com")
    auth_headers(email="receiver2@test.com")

    res = client.post(
        "/api/beneficiaries",
        json={"name": "Receiver", "account_email": "receiver2@test.com"},
        headers=sender_headers,
    )
    beneficiary_id = res.get_json()["id"]

    res = client.post(
        "/api/transactions/send",
        json={"beneficiary_id": beneficiary_id, "amount": 50},
        headers=sender_headers,
    )
    assert res.status_code == 400
