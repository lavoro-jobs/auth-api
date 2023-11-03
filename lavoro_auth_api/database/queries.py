import uuid

from lavoro_auth_api.database import db
from lavoro_library.models import UserInDB


def get_user_by_email(email: str):
    query_tuple = ("SELECT * FROM accounts WHERE email = %s", (email,))
    result = db.execute_one(query_tuple)
    if result["result"]:
        return UserInDB(**result["result"][0])
    else:
        return None


def get_user_by_verification_token(verification_token: str):
    query_tuple = (
        """
        SELECT * FROM verification_tokens
        JOIN accounts
        ON verification_tokens.account_id = accounts.id
        WHERE token = %s
        """,
        (verification_token,),
    )
    result = db.execute_one(query_tuple)
    if result["result"]:
        return UserInDB(**result["result"][0])
    else:
        return None


def set_active_account(user_id: uuid.UUID):
    query_tuple = (
        """
        UPDATE accounts
        SET is_active = TRUE
        WHERE id = %s
        """,
        (user_id,),
    )
    result = db.execute_one(query_tuple)
    return result["affected_rows"] == 1
