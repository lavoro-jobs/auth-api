from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field, SecretStr

from lavoro_auth_api.database.queries import (
    get_user_by_email,
    create_account,
)
from lavoro_auth_api.helpers.login_helpers import get_password_hash
from lavoro_auth_api.helpers.register_helpers import create_confirmation_token


class RegistrationForm(BaseModel):
    email: EmailStr = Field(examples=['marko.horvat@gmail.com']) # mozes maknut jer se to ne vidi na swaggeru ni nigdje (ili prepravit da se vidi)
    password: SecretStr = Field(
        json_schema_extra={
            'title': 'Password', # mozes maknut jer se to ne vidi na swaggeru ni nigdje (ili prepravit da se vidi)
            'description': 'Password of the user', # mozes maknut jer se to ne vidi na swaggeru ni nigdje (ili prepravit da se vidi)
        }
    )
    role: str = Field(
        examples=['applicant', 'recruiter'], # mozes maknut jer se to ne vidi na swaggeru ni nigdje (ili prepravit da se vidi)
        json_schema_extra={
            'title': 'Role', # mozes maknut jer se to ne vidi na swaggeru ni nigdje (ili prepravit da se vidi)
            'description': 'Role of the user', # mozes maknut jer se to ne vidi na swaggeru ni nigdje (ili prepravit da se vidi)
        }
    )


router = APIRouter(prefix="/register", tags=["register"])


@router.post("/")
def register_user(user: Annotated[RegistrationForm, Depends()]):
    user_exists = get_user_by_email(user.email)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )

    hashed_password = get_password_hash(user.password.get_secret_value())
    confirmation_token = create_confirmation_token()
    affected_rows = create_account(
        user.email, hashed_password, user.role, confirmation_token
    )
    # send_confirmation_email(username)
    return {"message": "User successfuly created"}
