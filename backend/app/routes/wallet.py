from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
from app.extensions import db
from app.models.wallet import Wallet
from app.models.transaction import Transaction

wallet_bp = Blueprint("wallet", __name__)


@wallet_bp.get("")
@jwt_required()
def get_wallet():
    user_id = get_jwt_identity()
    wallet = Wallet.query.filter_by(user_id=user_id).first_or_404()

    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    txns = Transaction.query.filter(
        or_(
            Transaction.sender_wallet_id == wallet.id,
            Transaction.receiver_wallet_id == wallet.id,
        )
    ).all()

    total_sent = sum(
        float(t.amount) for t in txns if t.sender_wallet_id == wallet.id
    )
    total_received = sum(
        float(t.amount) for t in txns if t.receiver_wallet_id == wallet.id
    )
    recent_count = sum(1 for t in txns if t.created_at >= thirty_days_ago)

    return jsonify({
        "wallet": wallet.to_dict(),
        "analytics": {
            "total_sent": round(total_sent, 2),
            "total_received": round(total_received, 2),
            "transaction_count": len(txns),
            "transactions_last_30_days": recent_count,
        },
    })


@wallet_bp.post("/add-funds")
@jwt_required()
def add_funds():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    amount = data.get("amount")

    if not amount or float(amount) <= 0:
        return jsonify({"error": "amount must be a positive number"}), 400

    wallet = Wallet.query.filter_by(user_id=user_id).first_or_404()
    wallet.balance = float(wallet.balance) + float(amount)

    txn = Transaction(
        sender_wallet_id=None,
        receiver_wallet_id=wallet.id,
        amount=amount,
        fee=0,
        type="deposit",
        status="completed",
    )
    db.session.add(txn)
    db.session.commit()

    return jsonify({"wallet": wallet.to_dict(), "transaction": txn.to_dict()}), 201
