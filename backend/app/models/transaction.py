from datetime import datetime
from app.extensions import db


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    sender_wallet_id = db.Column(db.Integer, db.ForeignKey("wallets.id"), nullable=True)
    receiver_wallet_id = db.Column(db.Integer, db.ForeignKey("wallets.id"), nullable=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    fee = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # "deposit" | "transfer"
    status = db.Column(db.String(20), default="completed", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sender_wallet = db.relationship("Wallet", foreign_keys=[sender_wallet_id])
    receiver_wallet = db.relationship("Wallet", foreign_keys=[receiver_wallet_id])

    @staticmethod
    def calculate_fee(amount, fee_percent, fee_cap):
        fee = float(amount) * fee_percent
        return round(min(fee, fee_cap), 2)

    def to_dict(self):
        return {
            "id": self.id,
            "sender_wallet_id": self.sender_wallet_id,
            "receiver_wallet_id": self.receiver_wallet_id,
            "amount": float(self.amount),
            "fee": float(self.fee),
            "type": self.type,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }
