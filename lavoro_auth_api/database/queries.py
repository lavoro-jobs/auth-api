from lavoro_auth_api.database import db
from lavoro_library.models import UserInDB

from datetime import datetime, timezone, timedelta


def get_user_by_email(email: str):
    result = db.execute_one(("SELECT * FROM accounts WHERE email = %s", (email,)))
    if result["result"]:
        return UserInDB(**result["result"][0])
    else:
        return None


def post_user_to_accounts_tokens(
    email: str,
    password_hash: str,
    role: str,
    token: str,
):
    accounts_tuple = (
        "INSERT INTO accounts (email, password_hash, role, is_active) VALUES (%s, %s, %s, TRUE)",
        (email, password_hash, role),
    )
    tokens_tuple = (
        "INSERT INTO verification_tokens (token, account_id) SELECT %s, id FROM accounts WHERE email = %s",
        (token, email),
    )

    result = db.execute_many([accounts_tuple, tokens_tuple])
    if result["affected_rows"]:
        print("#########################" + str(result["affected_rows"]))
        return result["affected_rows"]
    else:
        return None
