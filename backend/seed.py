"""
Run with: python seed.py
Creates the tables (if they don't exist) and seeds one admin and two demo users
so the frontend has data to work against immediately.
"""
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.wallet import Wallet
from app.models.beneficiary import Beneficiary

app = create_app()

with app.app_context():
    db.create_all()

    if not User.query.filter_by(email="admin@moneyapp.com").first():
        admin = User(full_name="Platform Admin", email="admin@moneyapp.com", is_admin=True)
        admin.set_password("Admin123!")
        db.session.add(admin)
        db.session.flush()
        db.session.add(Wallet(user_id=admin.id, balance=0))

    if not User.query.filter_by(email="oliver@example.com").first():
        oliver = User(full_name="Oliver Moosberger", email="oliver@example.com")
        oliver.set_password("Password123!")
        db.session.add(oliver)
        db.session.flush()
        db.session.add(Wallet(user_id=oliver.id, balance=1000))

    if not User.query.filter_by(email="jane@example.com").first():
        jane = User(full_name="Jane Wanjiru", email="jane@example.com")
        jane.set_password("Password123!")
        db.session.add(jane)
        db.session.flush()
        db.session.add(Wallet(user_id=jane.id, balance=250))

    db.session.commit()

    oliver = User.query.filter_by(email="oliver@example.com").first()
    jane = User.query.filter_by(email="jane@example.com").first()
    if oliver and jane and not Beneficiary.query.filter_by(owner_id=oliver.id).first():
        db.session.add(Beneficiary(owner_id=oliver.id, name="Jane", account_email=jane.email))
        db.session.commit()

    print("Seed complete. Demo logins:")
    print("  admin@moneyapp.com / Admin123!")
    print("  oliver@example.com / Password123!")
    print("  jane@example.com / Password123!")
