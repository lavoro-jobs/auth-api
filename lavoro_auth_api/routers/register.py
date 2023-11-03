from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from lavoro_auth_api.database.queries import (
    get_user_by_email,
    post_user_to_accounts_tokens,
)
from lavoro_auth_api.helpers.login_helpers import get_password_hash, create_access_token


router = APIRouter(prefix="/register", tags=["register"])


@router.post("/user")
def register_user(username: str, password: str, role: str):
    user = get_user_by_email(username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )

    hashed_password = get_password_hash(password)
    confirmation_token = create_access_token(
        data={"sub": username}, expires_delta=timedelta(days=1)
    )
    affected_rows = post_user_to_accounts_tokens(
        username, hashed_password, role, confirmation_token
    )
    return {"affected_rows": affected_rows}
