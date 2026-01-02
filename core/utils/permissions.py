from fastapi import HTTPException


def handle_user_permission(user_group: str, valid_groups: list):
    if user_group not in valid_groups:
        raise HTTPException(status_code=403, detail="Invalid group permission")
    return True