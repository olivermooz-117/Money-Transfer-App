from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models.user import User
from app.models.wallet import Wallet

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    data = request.get_json() or {}
    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")

    if not all([full_name, email, password]):
        return jsonify({"error": "full_name, email and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "An account with this email already exists"}), 409

    user = User(full_name=full_name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.flush()  # get user.id before commit

    # Every new user gets a wallet at 0 balance — removes the "needs a bank account" barrier
    wallet = Wallet(user_id=user.id, balance=0)
    db.session.add(wallet)
    db.session.commit()

    token = create_access_token(
        identity=str(user.id), additional_claims={"is_admin": user.is_admin}
    )
    return jsonify({"token": token, "user": user.to_dict(include_wallet=True)}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    if not user.is_active:
        return jsonify({"error": "This account has been deactivated"}), 403

    token = create_access_token(
        identity=str(user.id), additional_claims={"is_admin": user.is_admin}
    )
    return jsonify({"token": token, "user": user.to_dict(include_wallet=True)}), 200
