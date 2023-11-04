from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from lavoro_auth_api.database.queries import get_user_by_email
from lavoro_auth_api.helpers.confirmation_helpers import activate_user_account
from lavoro_auth_api.helpers.register_helpers import register_user
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
    confirmation_token = register_user(form_data.email, form_data.password.get_secret_value(), form_data.role)
    await send_confirmation_email(form_data.email, confirmation_token)
    return {"message": f"Email sent to {form_data.email}"}


@router.post("/confirm/{verification_token}")
def confirm_email(verification_token: str):
    activation_result = activate_user_account(verification_token)
    if activation_result:
        return {"message": "Account activated"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong verification token or account already activated"
        )
