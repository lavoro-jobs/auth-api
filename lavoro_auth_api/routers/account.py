from fastapi import APIRouter, Depends, HTTPException

# from lavoro_auth_api.database.queries import get_user_by_email
from lavoro_auth_api.services import account_service

# from lavoro_library.models import UserInDB
from lavoro_library.model.auth_api.db_models import Account

router = APIRouter(prefix="/account", tags=["account"])


@router.get("/{email}", response_model=Account)
def get_current_user(email: str):
    return account_service.get_account_by_email(email)
    # user = get_user_by_email(email)
    # if user:
    #     return user
    # else:
    #     raise HTTPException(status_code=404, detail="User not found")
