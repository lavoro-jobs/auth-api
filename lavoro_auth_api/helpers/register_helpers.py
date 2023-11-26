import secrets

from lavoro_auth_api.helpers.login_helpers import get_password_hash
from lavoro_auth_api.database.queries import create_account, create_account_no_confirm


def generate_confirmation_token():
    return secrets.token_urlsafe(32)


def register_user(email, password, role):
    confirmation_token = generate_confirmation_token()
    password_hash = get_password_hash(password)
    create_account(email, password_hash, role, confirmation_token)
    return confirmation_token


def register_user_no_confirm(email, password, role):
    password_hash = get_password_hash(password)
    create_account_no_confirm(email, password_hash, role)
    return {"detail": f"User {email} registered"}
