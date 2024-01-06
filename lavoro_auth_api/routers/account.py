import uuid
from fastapi import APIRouter

from lavoro_auth_api.services import account_service

from lavoro_library.model.auth_api.db_models import Account

router = APIRouter(prefix="/account", tags=["account"])


@router.get("/{email}", response_model=Account)
def get_current_user(email: str):
    return account_service.get_account_by_email(email)


@router.get("/get-stream-chat-token/{account_id}")
def get_account_by_id(account_id: uuid.UUID):
    return account_service.get_stream_chat_token(account_id)
