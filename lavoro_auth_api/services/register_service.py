import hashlib
import os
import secrets

import stream_chat
from fastapi import HTTPException, status

from lavoro_auth_api import common
from lavoro_auth_api.database import queries

from lavoro_library.model.auth_api.dtos import RegisterDTO


async def register(form_data: RegisterDTO):
    user = queries.get_account_by_email(form_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    confirmation_token = secrets.token_urlsafe(32)
    password_hash = common.get_password_hash(form_data.password)

    client = stream_chat.StreamChat(os.environ["STREAM_CHAT_API_KEY"], os.environ["STREAM_CHAT_API_SECRET"])
    stream_chat_token = client.create_token(hashlib.sha256(form_data.email.encode()).hexdigest())

    queries.create_account(form_data.email, password_hash, form_data.role, confirmation_token, stream_chat_token)
    return await common.send_confirmation_email(form_data.email, confirmation_token)


def register_no_confirm(form_data: RegisterDTO):
    user = queries.get_account_by_email(form_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    password_hash = common.get_password_hash(form_data.password)

    client = stream_chat.StreamChat(os.environ["STREAM_CHAT_API_KEY"], os.environ["STREAM_CHAT_API_SECRET"])
    stream_chat_token = client.create_token(form_data.email)

    queries.create_account_no_confirm(form_data.email, password_hash, form_data.role, stream_chat_token)
    return {"detail": f"User {form_data.email} registered and activated"}


def confirm_email(verification_token: str):
    exc = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Wrong verification token or account already activated",
    )
    user = queries.get_account_by_verification_token(verification_token)
    if not user:
        raise exc
    if user.is_active:
        raise exc

    result = queries.set_active_account(user.id)
    if not result:
        raise exc
    return {"detail": "Account activated"}
