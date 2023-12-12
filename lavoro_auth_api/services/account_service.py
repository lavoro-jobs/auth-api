from fastapi import HTTPException
from lavoro_auth_api.database import queries


def get_account_by_email(email: str):
    user = queries.get_account_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user
