from datetime import datetime
from decimal import Decimal
from app.extensions import db


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    sender_wallet_id = db.Column(db.Integer, db.ForeignKey("wallets.id"), nullable=True)
    receiver_wallet_id = db.Column(db.Integer, db.ForeignKey("wallets.id"), nullable=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    fee = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    type = db.Column(db.String(20), nullable=False)  # transfer, deposit
    status = db.Column(db.String(20), nullable=False, default="completed")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "sender_wallet_id": self.sender_wallet_id,
            "receiver_wallet_id": self.receiver_wallet_id,
            "amount": float(self.amount),
            "fee": float(self.fee),
            "type": self.type,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @staticmethod
    def calculate_fee(amount, percent, cap):
        amount = Decimal(str(amount))
        percent = Decimal(str(percent))
        cap = Decimal(str(cap))
        fee = amount * percent
        return min(fee, cap)