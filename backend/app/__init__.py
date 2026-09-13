from flask import Flask, jsonify
from app.config import Config
from app.extensions import db, migrate, jwt, bcrypt, cors


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # --- init extensions ---
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # --- import models so they register with SQLAlchemy before migrate/create_all ---
    from app.models import user, wallet, beneficiary, transaction  # noqa: F401

    # --- register blueprints ---
    from app.routes.auth import auth_bp
    from app.routes.users import users_bp
    from app.routes.wallet import wallet_bp
    from app.routes.beneficiaries import beneficiaries_bp
    from app.routes.transactions import transactions_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(wallet_bp, url_prefix="/api/wallet")
    app.register_blueprint(beneficiaries_bp, url_prefix="/api/beneficiaries")
    app.register_blueprint(transactions_bp, url_prefix="/api/transactions")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error"}), 500

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    return app
