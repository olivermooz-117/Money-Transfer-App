from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User

users_bp = Blueprint("users", __name__)


@users_bp.get("/me")
@jwt_required()
def get_me():
    user = User.query.get_or_404(get_jwt_identity())
    return jsonify(user.to_dict(include_wallet=True))


@users_bp.put("/me")
@jwt_required()
def update_me():
    user = User.query.get_or_404(get_jwt_identity())
    data = request.get_json() or {}

    if "full_name" in data:
        user.full_name = data["full_name"]
    if "email" in data:
        existing = User.query.filter_by(email=data["email"]).first()
        if existing and existing.id != user.id:
            return jsonify({"error": "Email already in use"}), 409
        user.email = data["email"]
    if "password" in data and data["password"]:
        user.set_password(data["password"])

    db.session.commit()
    return jsonify(user.to_dict(include_wallet=True))
