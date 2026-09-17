from unittest.mock import patch, MagicMock
from app.extensions import db
from app.models.user import User
from app.models.wallet import Wallet
from app.models.mpesa_deposit import MpesaDeposit


def test_normalize_phone_variants(app):
    from app.services.mpesa import normalize_phone

    with app.app_context():
        assert normalize_phone("0712345678") == "254712345678"
        assert normalize_phone("+254712345678") == "254712345678"
        assert normalize_phone("254712345678") == "254712345678"
        assert normalize_phone("712345678") == "254712345678"


def test_normalize_phone_invalid(app):
    from app.services.mpesa import normalize_phone

    with app.app_context():
        try:
            normalize_phone("12345")
            assert False, "expected ValueError"
        except ValueError:
            pass


@patch("app.services.mpesa.requests.post")
@patch("app.services.mpesa.requests.get")
def test_deposit_initiates_stk_and_saves_pending(mock_get, mock_post, client, auth_headers):
    mock_get.return_value = MagicMock(
        status_code=200,
        json=lambda: {"access_token": "fake-token"},
    )
    mock_get.return_value.raise_for_status = lambda: None

    mock_post.return_value = MagicMock(
        status_code=200,
        json=lambda: {
            "MerchantRequestID": "m-1",
            "CheckoutRequestID": "ws_CO_TEST_001",
            "ResponseCode": "0",
            "CustomerMessage": "Success. Request accepted for processing",
        },
    )

    headers = auth_headers(email="mpesa1@test.com")
    res = client.post(
        "/api/mpesa/deposit",
        json={"phone": "0712345678", "amount": 100},
        headers=headers,
    )
    assert res.status_code == 201
    body = res.get_json()
    assert body["deposit"]["status"] == "pending"
    assert body["deposit"]["checkout_request_id"] == "ws_CO_TEST_001"
    assert body["deposit"]["phone"] == "254712345678"


def test_deposit_rejects_invalid_phone(client, auth_headers):
    headers = auth_headers(email="mpesa_bad_phone@test.com")
    res = client.post(
        "/api/mpesa/deposit",
        json={"phone": "123", "amount": 10},
        headers=headers,
    )
    assert res.status_code == 400


def test_deposit_rejects_non_positive_amount(client, auth_headers):
    headers = auth_headers(email="mpesa_bad_amt@test.com")
    res = client.post(
        "/api/mpesa/deposit",
        json={"phone": "0712345678", "amount": 0},
        headers=headers,
    )
    assert res.status_code == 400


def test_callback_success_credits_wallet(client, auth_headers, app):
    headers = auth_headers(email="mpesa2@test.com")

    with app.app_context():
        user = User.query.filter_by(email="mpesa2@test.com").first()
        deposit = MpesaDeposit(
            user_id=user.id,
            phone="254712345678",
            amount=50,
            checkout_request_id="ws_CO_SUCCESS_1",
            merchant_request_id="m-2",
            status="pending",
        )
        db.session.add(deposit)
        db.session.commit()
        bal_before = float(Wallet.query.filter_by(user_id=user.id).first().balance)

    payload = {
        "Body": {
            "stkCallback": {
                "MerchantRequestID": "m-2",
                "CheckoutRequestID": "ws_CO_SUCCESS_1",
                "ResultCode": 0,
                "ResultDesc": "The service request is processed successfully.",
                "CallbackMetadata": {
                    "Item": [
                        {"Name": "Amount", "Value": 50},
                        {"Name": "MpesaReceiptNumber", "Value": "ABC123XYZ"},
                        {"Name": "PhoneNumber", "Value": 254712345678},
                    ]
                },
            }
        }
    }
    res = client.post("/api/mpesa/callback", json=payload)
    assert res.status_code == 200
    assert res.get_json()["ResultCode"] == 0

    with app.app_context():
        deposit = MpesaDeposit.query.filter_by(checkout_request_id="ws_CO_SUCCESS_1").first()
        assert deposit.status == "success"
        assert deposit.mpesa_receipt == "ABC123XYZ"
        wallet = Wallet.query.filter_by(user_id=user.id).first()
        assert float(wallet.balance) == bal_before + 50


def test_callback_failed_does_not_credit(client, auth_headers, app):
    headers = auth_headers(email="mpesa3@test.com")

    with app.app_context():
        user = User.query.filter_by(email="mpesa3@test.com").first()
        deposit = MpesaDeposit(
            user_id=user.id,
            phone="254712345678",
            amount=20,
            checkout_request_id="ws_CO_FAIL_1",
            status="pending",
        )
        db.session.add(deposit)
        db.session.commit()
        bal_before = float(Wallet.query.filter_by(user_id=user.id).first().balance)

    payload = {
        "Body": {
            "stkCallback": {
                "CheckoutRequestID": "ws_CO_FAIL_1",
                "ResultCode": 1032,
                "ResultDesc": "Request cancelled by user",
            }
        }
    }
    client.post("/api/mpesa/callback", json=payload)

    with app.app_context():
        deposit = MpesaDeposit.query.filter_by(checkout_request_id="ws_CO_FAIL_1").first()
        assert deposit.status == "failed"
        wallet = Wallet.query.filter_by(user_id=user.id).first()
        assert float(wallet.balance) == bal_before


def test_callback_idempotent(client, auth_headers, app):
    headers = auth_headers(email="mpesa4@test.com")

    with app.app_context():
        user = User.query.filter_by(email="mpesa4@test.com").first()
        wallet = Wallet.query.filter_by(user_id=user.id).first()
        wallet.balance = 100
        deposit = MpesaDeposit(
            user_id=user.id,
            phone="254712345678",
            amount=30,
            checkout_request_id="ws_CO_IDEM_1",
            status="success",
            mpesa_receipt="OLD",
        )
        db.session.add(deposit)
        db.session.commit()
        bal_before = float(wallet.balance)

    payload = {
        "Body": {
            "stkCallback": {
                "CheckoutRequestID": "ws_CO_IDEM_1",
                "ResultCode": 0,
                "ResultDesc": "ok",
                "CallbackMetadata": {
                    "Item": [
                        {"Name": "Amount", "Value": 30},
                        {"Name": "MpesaReceiptNumber", "Value": "NEW"},
                    ]
                },
            }
        }
    }
    client.post("/api/mpesa/callback", json=payload)

    with app.app_context():
        wallet = Wallet.query.filter_by(user_id=user.id).first()
        assert float(wallet.balance) == bal_before  # not credited again


def test_deposit_status_owner_only(client, auth_headers, app):
    h1 = auth_headers(email="owner@test.com")
    h2 = auth_headers(email="other@test.com")

    with app.app_context():
        owner = User.query.filter_by(email="owner@test.com").first()
        db.session.add(
            MpesaDeposit(
                user_id=owner.id,
                phone="254712345678",
                amount=10,
                checkout_request_id="ws_CO_OWN_1",
                status="pending",
            )
        )
        db.session.commit()

    res = client.get("/api/mpesa/deposit/ws_CO_OWN_1", headers=h1)
    assert res.status_code == 200
    assert res.get_json()["checkout_request_id"] == "ws_CO_OWN_1"

    res = client.get("/api/mpesa/deposit/ws_CO_OWN_1", headers=h2)
    assert res.status_code == 403