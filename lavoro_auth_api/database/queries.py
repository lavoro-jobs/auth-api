import uuid

from lavoro_auth_api.database import db

# from lavoro_library.models import UserInDB
from lavoro_library.model.auth_api.db_models import Account


def get_user_by_email(email: str):
    query_tuple = ("SELECT * FROM accounts WHERE email = %s", (email,))
    result = db.execute_one(query_tuple)
    if result["result"]:
        return Account(**result["result"][0])
    else:
        return None


def get_user_by_verification_token(verification_token: str):
    query_tuple = (
        """
        SELECT * FROM verification_tokens
        JOIN accounts
        ON verification_tokens.account_id = accounts.id
        WHERE token = %s AND expiry_date > NOW()
        """,
        (verification_token,),
    )
    result = db.execute_one(query_tuple)
    if result["result"]:
        return Account(**result["result"][0])
    else:
        return None


def create_account(
    email: str,
    password_hash: str,
    role: str,
    token: str,
):
    accounts_tuple = (
        "INSERT INTO accounts (email, password_hash, role, is_active) VALUES (%s, %s, %s, FALSE)",
        (email, password_hash, role),
    )
    tokens_tuple = (
        "INSERT INTO verification_tokens (token, account_id) SELECT %s, id FROM accounts WHERE email = %s",
        (token, email),
    )

    result = db.execute_many([accounts_tuple, tokens_tuple])
    if result["affected_rows"]:
        return result["affected_rows"]
    else:
        return None


def create_account_no_confirm(
    email: str,
    password_hash: str,
    role: str,
):
    query_tuple = (
        "INSERT INTO accounts (email, password_hash, role, is_active) VALUES (%s, %s, %s, TRUE)",
        (email, password_hash, role),
    )

    result = db.execute_one(query_tuple)
    if result["affected_rows"]:
        return result["affected_rows"]
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
