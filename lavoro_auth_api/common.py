from datetime import datetime
import os

from typing import Union
from datetime import timedelta, timezone

from jose import jwt

from passlib.context import CryptContext

from lavoro_auth_api.database.queries import get_account_by_email
from lavoro_library.email import send_email


SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, password_hash):
    return pwd_context.verify(plain_password, password_hash)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(email: str, password: str):
    user = get_account_by_email(email)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def send_confirmation_email(email, token):
    message_html = f"""
    <html>
        <body>
            <h1>Confirm your email</h1>
            <p>Please confirm your email by clicking on the link: <a href="http://localhost:3000/confirm-email/{token}">http://localhost:3000/confirm-email/{token}</a></p>
        </body>
    </html>
    """
    await send_email(email, "Lavoro - Confirm your email", message_html)
    return {"detail": "Confirmation email sent"}
