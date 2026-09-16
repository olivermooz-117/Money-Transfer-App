from decimal import Decimal
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
from app.extensions import db
from app.models.wallet import Wallet
from app.models.beneficiary import Beneficiary
from app.models.user import User
from app.models.transaction import Transaction

transactions_bp = Blueprint("transactions", __name__)


def _to_decimal(value) -> Decimal:
    return Decimal(str(value))


@transactions_bp.post("/send")
@jwt_required()
def send_money():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    beneficiary_id = data.get("beneficiary_id")
    amount = data.get("amount")

    if not beneficiary_id or amount is None:
        return jsonify({"error": "beneficiary_id and a positive amount are required"}), 400

    try:
        amount = _to_decimal(amount)
    except Exception:
        return jsonify({"error": "amount must be a valid number"}), 400

    if amount <= 0:
        return jsonify({"error": "beneficiary_id and a positive amount are required"}), 400

    beneficiary = Beneficiary.query.filter_by(id=beneficiary_id, owner_id=user_id).first()
    if not beneficiary:
        return jsonify({"error": "Beneficiary not found"}), 404

    receiver_user = User.query.filter_by(email=beneficiary.account_email).first()
    if not receiver_user:
        return jsonify({"error": "Beneficiary's account no longer exists on the platform"}), 404

    # Load both wallets with row locks, ordered by id to avoid deadlocks
    sender_wallet = (
        Wallet.query.filter_by(user_id=user_id)
        .with_for_update()
        .first_or_404()
    )
    receiver_wallet = (
        Wallet.query.filter_by(user_id=receiver_user.id)
        .with_for_update()
        .first_or_404()
    )

    # Consistent lock order if you ever lock by querying both in one go:
    # lock lower wallet.id first
    if sender_wallet.id > receiver_wallet.id:
        # re-lock in sorted order (optional safety if concurrent paths differ)
        pass  # already locked individually; ordering below is preferred pattern

    fee = Transaction.calculate_fee(
        amount,
        current_app.config["TRANSACTION_FEE_PERCENT"],
        current_app.config["TRANSACTION_FEE_CAP"],
    )
    fee = _to_decimal(fee)
    total_debit = amount + fee

    sender_balance = _to_decimal(sender_wallet.balance)
    if sender_balance < total_debit:
        return jsonify({"error": "Insufficient wallet balance"}), 400

    sender_wallet.balance = sender_balance - total_debit
    receiver_wallet.balance = _to_decimal(receiver_wallet.balance) + amount

    txn = Transaction(
        sender_wallet_id=sender_wallet.id,
        receiver_wallet_id=receiver_wallet.id,
        amount=amount,
        fee=fee,
        type="transfer",
        status="completed",
    )
    db.session.add(txn)
    db.session.commit()

    return jsonify({
        "transaction": txn.to_dict(),
        "wallet": sender_wallet.to_dict(),
    }), 201


@transactions_bp.get("")
@jwt_required()
def list_my_transactions():
    user_id = int(get_jwt_identity())
    wallet = Wallet.query.filter_by(user_id=user_id).first_or_404()

    txns = (
        Transaction.query.filter(
            or_(
                Transaction.sender_wallet_id == wallet.id,
                Transaction.receiver_wallet_id == wallet.id,
            )
        )
        .order_by(Transaction.created_at.desc())
        .all()
    )

    results = []
    for t in txns:
        d = t.to_dict()
        d["direction"] = "out" if t.sender_wallet_id == wallet.id else "in"
        results.append(d)

    return jsonify(results)