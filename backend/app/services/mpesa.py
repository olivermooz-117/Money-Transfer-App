import base64
import re
from datetime import datetime
import requests
from flask import current_app
from requests.auth import HTTPBasicAuth


def get_access_token():
    """Get OAuth access token from Daraja API."""
    consumer_key = current_app.config.get("MPESA_CONSUMER_KEY")
    consumer_secret = current_app.config.get("MPESA_CONSUMER_SECRET")
    base_url = current_app.config.get("MPESA_BASE_URL")

    if not consumer_key or not consumer_secret:
        raise RuntimeError("MPESA_CONSUMER_KEY and MPESA_CONSUMER_SECRET must be set")

    url = f"{base_url}/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret), timeout=30)
    response.raise_for_status()
    data = response.json()
    return data.get("access_token")


def normalize_phone(phone: str) -> str:
    """
    Normalize Kenyan phone number to 2547XXXXXXXX format.
    Accepts: 07XXXXXXXX, +2547XXXXXXXX, 2547XXXXXXXX, 07XX XXXXXXX, etc.
    """
    # Remove spaces, dashes, parentheses
    cleaned = re.sub(r"[\s\-\(\)]", "", phone)

    # Handle +254 prefix
    if cleaned.startswith("+254"):
        cleaned = cleaned[1:]  # remove +

    # Handle 07 prefix
    if cleaned.startswith("07"):
        cleaned = "254" + cleaned[1:]

    # Handle 7 prefix (without country code)
    if cleaned.startswith("7") and len(cleaned) == 9:
        cleaned = "254" + cleaned

    # Validate final format: 2547XXXXXXXX (12 digits)
    if not re.match(r"^2547\d{8}$", cleaned):
        raise ValueError(
            "Invalid phone number. Use format: 07XXXXXXXX, 2547XXXXXXXX, or +2547XXXXXXXX"
        )

    return cleaned


def stk_push(phone: str, amount: float, account_reference: str, description: str = "Wallet top-up"):
    """
    Initiate STK Push (CustomerPayBillOnline) via Daraja API.
    Returns Daraja JSON response containing CheckoutRequestID, MerchantRequestID, etc.
    """
    access_token = get_access_token()
    base_url = current_app.config.get("MPESA_BASE_URL")
    shortcode = current_app.config.get("MPESA_SHORTCODE")
    passkey = current_app.config.get("MPESA_PASSKEY")
    callback_url = current_app.config.get("MPESA_CALLBACK_URL")

    if not all([shortcode, passkey, callback_url]):
        raise RuntimeError("MPESA_SHORTCODE, MPESA_PASSKEY, and MPESA_CALLBACK_URL must be set")

    # Build timestamp and password
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password_str = f"{shortcode}{passkey}{timestamp}"
    password = base64.b64encode(password_str.encode()).decode()

    # Normalize phone
    normalized_phone = normalize_phone(phone)

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),  # Daraja expects integer amount
        "PartyA": normalized_phone,
        "PartyB": shortcode,
        "PhoneNumber": normalized_phone,
        "CallBackURL": callback_url,
        "AccountReference": account_reference,
        "TransactionDesc": description,
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    url = f"{base_url}/mpesa/stkpush/v1/processrequest"
    response = requests.post(url, json=payload, headers=headers, timeout=30)

    if response.status_code != 200:
        try:
            error_data = response.json()
            error_msg = error_data.get("errorMessage") or error_data.get("message") or response.text
        except Exception:
            error_msg = response.text
        raise RuntimeError(f"STK Push failed: {error_msg}")

    data = response.json()

    # Check for Daraja error response
    if "errorCode" in data:
        raise RuntimeError(f"STK Push error: {data.get('errorMessage')}")

    return data