from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from lavoro_auth_api.database.queries import get_user_by_email
from lavoro_auth_api.helpers.confirmation_helpers import activate_user_account
from lavoro_auth_api.helpers.register_helpers import register_user, register_user_no_confirm
from lavoro_auth_api.helpers.email_helpers import send_confirmation_email
from lavoro_library.models import RegistrationForm


router = APIRouter(prefix="/register", tags=["register"])


@router.post("")
async def register(form_data: Annotated[RegistrationForm, Depends()]):
    user = get_user_by_email(form_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    confirmation_token = register_user(form_data.email, form_data.password, form_data.role)
    await send_confirmation_email(form_data.email, confirmation_token)
    return {"detail": f"Email sent to {form_data.email}"}


@router.post("/no-confirm")
def register_no_confirm(form_data: Annotated[RegistrationForm, Depends()]):
    user = get_user_by_email(form_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    register_user_no_confirm(form_data.email, form_data.password, form_data.role)
    return {"detail": f"User {form_data.email} registered and activated"}

@router.post("/confirm/{verification_token}")
def confirm_email(verification_token: str):
    activation_result = activate_user_account(verification_token)
    if activation_result:
        return {"detail": "Account activated"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong verification token or account already activated"
        )
