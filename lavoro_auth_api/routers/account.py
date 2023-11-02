from fastapi import APIRouter, Depends, HTTPException

from lavoro_auth_api.database.queries import get_user_by_email

from lavoro_library.models import UserInDB


router = APIRouter(prefix="/account", tags=["account"])


@router.get("/{email}", response_model=UserInDB)
def get_current_user(email: str):
    user = get_user_by_email(email)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")
