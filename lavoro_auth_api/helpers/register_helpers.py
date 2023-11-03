import secrets

def create_confirmation_token():
    return secrets.token_urlsafe(32)
