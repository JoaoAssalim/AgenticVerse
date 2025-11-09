import logging
from fastapi import APIRouter, HTTPException

from models.users import UserLoginModel
from core.api.users import UsersAPIView
from core.auth.utils import verify_password

logger = logging.Logger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.post("/login")
async def login(user: UserLoginModel):
    logger.info(f"Authenticating user {user.email}")
    user_db = UsersAPIView().get_user_by_email(user.email)

    if not verify_password(user.password, user_db.password):
        logger.error(f"Error to authenticate user {user.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    
    return {"api_key": user_db.api_key}