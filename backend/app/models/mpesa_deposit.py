from datetime import datetime, timezone
from app.extensions import db


class MpesaDeposit(db.Model):
    __tablename__ = "mpesa_deposits"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    checkout_request_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    merchant_request_id = db.Column(db.String(50), nullable=True)
    mpesa_receipt = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), default="pending", nullable=False)  # pending, success, failed
    result_desc = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user = db.relationship("User", backref=db.backref("mpesa_deposits", lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "phone": self.phone,
            "amount": float(self.amount),
            "checkout_request_id": self.checkout_request_id,
            "merchant_request_id": self.merchant_request_id,
            "mpesa_receipt": self.mpesa_receipt,
            "status": self.status,
            "result_desc": self.result_desc,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }