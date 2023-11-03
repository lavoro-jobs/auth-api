import secrets

from lavoro_auth_api.helpers.login_helpers import get_password_hash
from lavoro_auth_api.database.queries import create_account


def generate_confirmation_token():
    return secrets.token_urlsafe(32)


def register_user(email, password, role):
    confirmation_token = generate_confirmation_token()
    password_hash = get_password_hash(password)
    create_account(email, password_hash, role, confirmation_token)
    return confirmation_token
