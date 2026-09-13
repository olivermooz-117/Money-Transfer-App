from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.beneficiary import Beneficiary
from app.models.user import User

beneficiaries_bp = Blueprint("beneficiaries", __name__)


@beneficiaries_bp.get("")
@jwt_required()
def list_beneficiaries():
    user_id = get_jwt_identity()
    beneficiaries = Beneficiary.query.filter_by(owner_id=user_id).all()
    return jsonify([b.to_dict() for b in beneficiaries])


@beneficiaries_bp.post("")
@jwt_required()
def add_beneficiary():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    name = data.get("name")
    account_email = data.get("account_email")

    if not all([name, account_email]):
        return jsonify({"error": "name and account_email are required"}), 400

    if account_email == User.query.get(user_id).email:
        return jsonify({"error": "You cannot add yourself as a beneficiary"}), 400

    if not User.query.filter_by(email=account_email).first():
        return jsonify({"error": "No platform user found with that email"}), 404

    beneficiary = Beneficiary(owner_id=user_id, name=name, account_email=account_email)
    db.session.add(beneficiary)
    db.session.commit()
    return jsonify(beneficiary.to_dict()), 201


@beneficiaries_bp.delete("/<int:beneficiary_id>")
@jwt_required()
def delete_beneficiary(beneficiary_id):
    user_id = get_jwt_identity()
    beneficiary = Beneficiary.query.filter_by(id=beneficiary_id, owner_id=user_id).first_or_404()
    db.session.delete(beneficiary)
    db.session.commit()
    return jsonify({"message": "Beneficiary removed"}), 200
