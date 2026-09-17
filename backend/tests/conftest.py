import pytest
from app import create_app
from app.extensions import db as _db
from app.config import Config


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    MPESA_ENV = "sandbox"
    MPESA_CONSUMER_KEY = "test-key"
    MPESA_CONSUMER_SECRET = "test-secret"
    MPESA_SHORTCODE = "174379"
    MPESA_PASSKEY = "test-passkey"
    MPESA_CALLBACK_URL = "https://example.com/api/mpesa/callback"
    MPESA_BASE_URL = "https://sandbox.safaricom.co.ke"


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    """Registers a fresh user and returns Authorization headers for it."""
    def _make(email="user@test.com", password="Password123!"):
        client.post(
            "/api/auth/register",
            json={"full_name": "Test User", "email": email, "password": password},
        )
        res = client.post("/api/auth/login", json={"email": email, "password": password})
        token = res.get_json()["token"]
        return {"Authorization": f"Bearer {token}"}
    return _make