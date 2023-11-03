from enum import Enum
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, SecretStr

from lavoro_auth_api.database.queries import get_user_by_email
from lavoro_auth_api.helpers.register_helpers import register_user
from lavoro_auth_api.helpers.email_helpers import send_confirmation_email


class Role(str, Enum):
    applicant = "applicant"
    employer = "employer"


class RegistrationForm(BaseModel):
    email: EmailStr
    password: SecretStr
    role: Role


router = APIRouter(prefix="/register", tags=["register"])


@router.post("")
async def register(form_data: Annotated[RegistrationForm, Depends()]):
    user = get_user_by_email(form_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    confirmation_token = register_user(form_data.email, form_data.password.get_secret_value(), form_data.role)
    await send_confirmation_email(form_data.email, confirmation_token)
    return {"message": f"Email sent to {form_data.email}"}
