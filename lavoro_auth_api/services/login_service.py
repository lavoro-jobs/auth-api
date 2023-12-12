from datetime import timedelta
from fastapi import HTTPException, status
from lavoro_auth_api import common
from lavoro_library.model.auth_api.dtos import LoginDTO

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def login(form_data: LoginDTO):
    user = common.authenticate_user(form_data.username, form_data.password)
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
    access_token = common.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
