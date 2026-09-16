from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import exc
from decimal import Decimal
from app.extensions import db
from app.models.mpesa_deposit import MpesaDeposit
from app.models.wallet import Wallet
from app.models.transaction import Transaction
from app.services.mpesa import stk_push, normalize_phone

mpesa_bp = Blueprint("mpesa", __name__)


@mpesa_bp.post("/deposit")
@jwt_required()
def initiate_deposit():
    """Initiate M-Pesa STK Push for wallet top-up."""
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    phone = data.get("phone")
    amount = data.get("amount")

    if not phone:
        return jsonify({"error": "phone is required"}), 400
    if not amount or float(amount) <= 0:
        return jsonify({"error": "amount must be a positive number"}), 400
    if float(amount) < 1:
        return jsonify({"error": "amount must be at least 1"}), 400

    try:
        normalized_phone = normalize_phone(phone)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # Initiate STK Push
    account_reference = f"U{user_id}"
    try:
        response = stk_push(
            phone=normalized_phone,
            amount=float(amount),
            account_reference=account_reference,
            description="Wallet top-up"
        )
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 502

    checkout_request_id = response.get("CheckoutRequestID")
    merchant_request_id = response.get("MerchantRequestID")

    if not checkout_request_id:
        return jsonify({"error": "Failed to get CheckoutRequestID from M-Pesa", "details": response}), 502

    # Save deposit record with pending status
    deposit = MpesaDeposit(
        user_id=user_id,
        phone=normalized_phone,
        amount=amount,
        checkout_request_id=checkout_request_id,
        merchant_request_id=merchant_request_id,
        status="pending",
    )
    db.session.add(deposit)
    db.session.commit()

    return jsonify({
        "deposit": deposit.to_dict(),
        "message": "STK Push sent. Check your phone and enter M-Pesa PIN.",
        "customer_message": response.get("CustomerMessage")
    }), 201


@mpesa_bp.post("/callback")
def mpesa_callback():
    """Safaricom Daraja callback for STK Push result."""
    data = request.get_json() or {}
    callback = data.get("Body", {}).get("stkCallback", {})

    if not callback:
        current_app.logger.warning("Invalid callback payload: %s", data)
        return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})

    checkout_request_id = callback.get("CheckoutRequestID")
    result_code = callback.get("ResultCode")
    result_desc = callback.get("ResultDesc", "")

    deposit = MpesaDeposit.query.filter_by(checkout_request_id=checkout_request_id).first()
    if not deposit:
        current_app.logger.warning("Deposit not found for CheckoutRequestID: %s", checkout_request_id)
        return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})

    # Already processed - return early
    if deposit.status == "success":
        return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})

    deposit.result_desc = result_desc

    if result_code == 0:
        # Success - extract receipt and amount from CallbackMetadata
        metadata = callback.get("CallbackMetadata", {}).get("Item", [])
        mpesa_receipt = None
        received_amount = None

        for item in metadata:
            if item.get("Name") == "MpesaReceiptNumber":
                mpesa_receipt = item.get("Value")
            elif item.get("Name") == "Amount":
                received_amount = item.get("Value")

        deposit.mpesa_receipt = mpesa_receipt
        deposit.status = "success"

        # Credit wallet atomically
        try:
            wallet = Wallet.query.filter_by(user_id=deposit.user_id).with_for_update().first()
            if wallet:
                # Prefer received_amount from callback metadata, fallback to deposit.amount
                credit_amount = Decimal(str(received_amount)) if received_amount is not None else deposit.amount
                wallet.balance = Decimal(str(wallet.balance)) + credit_amount

                # Create transaction record
                txn = Transaction(
                    sender_wallet_id=None,
                    receiver_wallet_id=wallet.id,
                    amount=credit_amount,
                    fee=0,
                    type="deposit",
                    status="completed",
                )
                db.session.add(txn)
            else:
                current_app.logger.error("Wallet not found for user_id: %s", deposit.user_id)
                deposit.status = "failed"
        except exc.SQLAlchemyError as e:
            current_app.logger.exception("Failed to credit wallet: %s", e)
            deposit.status = "failed"
    else:
        deposit.status = "failed"

    db.session.commit()
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})


@mpesa_bp.get("/deposit/<checkout_request_id>")
@jwt_required()
def get_deposit_status(checkout_request_id):
    """Poll deposit status by CheckoutRequestID (owner only)."""
    user_id = int(get_jwt_identity())
    deposit = MpesaDeposit.query.filter_by(checkout_request_id=checkout_request_id).first()

    if not deposit:
        return jsonify({"error": "Deposit not found"}), 404
    if deposit.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    return jsonify(deposit.to_dict())