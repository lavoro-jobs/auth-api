from fastapi import APIRouter, HTTPException, status

from lavoro_auth_api.helpers.confirmation_helpers import activate_user_account


router = APIRouter(prefix="/register", tags=["register"])


@router.post("/confirm/{verification_token}}")
def confirm_email(verification_token: str):
    activation_result = activate_user_account(verification_token)
    if activation_result:
        return {"message": "Account activated"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong verification token or account already activated"
        )
