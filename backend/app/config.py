import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/money_transfer_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 8  # 8 hours

    # Business rule: keep fees low to address the "high transaction fees" problem
    TRANSACTION_FEE_PERCENT = 0.01   # 1%
    TRANSACTION_FEE_CAP = 100.0      # never charge more than this, in wallet currency units
