from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from lavoro_auth_api.helpers.login_helpers import authenticate_user, create_access_token

# from lavoro_library.models import LoginForm, Token
from lavoro_library.model.auth_api.dtos import LoginDTO, TokenDTO


router = APIRouter(prefix="/login", tags=["login"])


ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/token", response_model=TokenDTO)
def login_for_access_token(form_data: Annotated[LoginDTO, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password. If you have not verified your email, please do so before logging in.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account inactive. Please verify your email before logging in.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
