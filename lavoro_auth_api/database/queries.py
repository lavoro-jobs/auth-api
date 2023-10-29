from lavoro_auth_api.database import db
from lavoro_library.models import UserInDB


def get_user_by_email(email: str):
    result = db.execute_query("SELECT * FROM account WHERE email = %s", (email,))
    if result["result"]:
        return UserInDB(**result["result"][0])
    else:
        return None
