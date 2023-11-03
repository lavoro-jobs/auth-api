from fastapi import APIRouter, HTTPException, status

from lavoro_auth_api.database.queries import (
    get_user_by_email,
    create_account,
)
from lavoro_auth_api.helpers.login_helpers import get_password_hash
from lavoro_auth_api.helpers.register_helpers import create_confirmation_token


router = APIRouter(prefix="/register", tags=["register"])


@router.post("/")
def register_user(username: str, password: str, role: str):
    user = get_user_by_email(username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )

    hashed_password = get_password_hash(password)
    confirmation_token = create_confirmation_token()
    affected_rows = create_account(
        username, hashed_password, role, confirmation_token
    )
    # send_confirmation_email(username)
    return {"message": "User successfuly created"}
