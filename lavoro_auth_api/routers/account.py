from fastapi import APIRouter, Depends, HTTPException, status

from lavoro_auth_api.database import db
from lavoro_auth_api.database.queries import get_user_by_email

from lavoro_library.models import UserInDB


router = APIRouter(prefix="/account", tags=["account"])


@router.get("/{email}")
def get_current_user(email: str):
    result = get_user_by_email(email)
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail="User not found")
