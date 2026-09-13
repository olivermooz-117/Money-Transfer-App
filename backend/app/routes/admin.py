from datetime import datetime
from flask import Blueprint, request, jsonify
from sqlalchemy import func, extract
from app.extensions import db
from app.models.user import User
from app.models.wallet import Wallet
from app.models.transaction import Transaction
from app.utils.decorators import admin_required

admin_bp = Blueprint("admin", __name__)


# ---------- Users ----------

@admin_bp.get("/users")
@admin_required
def list_users():
    users = User.query.all()
    return jsonify([u.to_dict(include_wallet=True) for u in users])


@admin_bp.put("/users/<int:user_id>")
@admin_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json() or {}

    if "full_name" in data:
        user.full_name = data["full_name"]
    if "is_admin" in data:
        user.is_admin = bool(data["is_admin"])
    if "is_active" in data:
        user.is_active = bool(data["is_active"])

    db.session.commit()
    return jsonify(user.to_dict(include_wallet=True))


@admin_bp.delete("/users/<int:user_id>")
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})


# ---------- Transactions ----------

@admin_bp.get("/transactions")
@admin_required
def all_transactions():
    txns = Transaction.query.order_by(Transaction.created_at.desc()).all()
    return jsonify([t.to_dict() for t in txns])


# ---------- Analytics ----------

@admin_bp.get("/analytics")
@admin_required
def wallet_analytics():
    total_users = User.query.count()
    total_balance = db.session.query(func.coalesce(func.sum(Wallet.balance), 0)).scalar()
    total_volume = db.session.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.type == "transfer"
    ).scalar()
    total_fees_collected = db.session.query(func.coalesce(func.sum(Transaction.fee), 0)).scalar()

    return jsonify({
        "total_users": total_users,
        "total_wallet_balance": float(total_balance),
        "total_transfer_volume": float(total_volume),
        "total_fees_collected": float(total_fees_collected),
    })


@admin_bp.get("/profit-trends")
@admin_required
def profit_trends():
    """Monthly fee revenue, used to spot trends for future decision-making."""
    rows = (
        db.session.query(
            extract("year", Transaction.created_at).label("year"),
            extract("month", Transaction.created_at).label("month"),
            func.sum(Transaction.fee).label("total_fees"),
            func.count(Transaction.id).label("transaction_count"),
        )
        .filter(Transaction.type == "transfer")
        .group_by("year", "month")
        .order_by("year", "month")
        .all()
    )

    return jsonify([
        {
            "year": int(r.year),
            "month": int(r.month),
            "total_fees": float(r.total_fees or 0),
            "transaction_count": r.transaction_count,
        }
        for r in rows
    ])
