from auth_api.database import db


def get_user_by_email(email: str):
    result = db.execute_query(
        "SELECT * FROM account WHERE email = %s", (email,))
    return result["result"]