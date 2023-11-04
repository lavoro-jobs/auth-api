from lavoro_auth_api.database.queries import set_active_account, get_user_by_verification_token


def activate_user_account(verification_token: str):
    user = get_user_by_verification_token(verification_token)
    if not user:
        return False
    if user.is_active:
        return False

    return set_active_account(user.id)
