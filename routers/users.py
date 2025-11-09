import logging
from fastapi import APIRouter, HTTPException, Depends

from core.auth import validate_api_key
from core.api.users import UsersAPIView
from database.models.users import UserModel
from models.users import UserBaseModel, UserUpdateModel, UserResponseModel

logger = logging.Logger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/create")
def create_user(user: UserBaseModel):
    logger.info(f"Creating user: {user.email}")
    try:
        user_model = user.model_dump_json(exclude_unset=True)
        user_model = UserModel.model_validate_json(user_model)
        return UsersAPIView().create_user(user_model)
    except HTTPException as e:
        logger.error(f"Error to create user: {user.email}")
        raise f"Error to create user: {e}"

@router.patch("/update/{user_id}")
def update_user(user_id: str, user_data: UserUpdateModel, user: UserModel = Depends(validate_api_key)):
    logger.info(f"Updating user: {user_id}")

    try:
        user_model = user_data.model_dump_json(exclude_unset=True)
        user_model = UserModel.model_validate_json(user_model)
        return UsersAPIView().update_user(user_id, user_model)
    except HTTPException as e:
        logger.error(f"Error updating user: {user_id}")
        raise f"Error to update user {user_id}: {e}"

@router.get("/get/{user_id}")
def get_user(user_id: str, user: UserModel = Depends(validate_api_key)):
    logger.info(f"Getting user: {user_id}")
    try:
        user_model = UsersAPIView().get_user(user_id)
        user_model = UserResponseModel.model_validate_json(user_model.model_dump_json())
        return user_model
    except HTTPException as e:
        logger.error(f"Error getting user: {user_id}")
        raise f"Error to get user {user_id}: {e}"

@router.get("/get-all")
def get_all_users(user: UserModel = Depends(validate_api_key)):
    logger.info("Getting all users")
    try:
        users_model = UsersAPIView().get_all_users()
        users_model = [UserResponseModel.model_validate_json(user_model.model_dump_json()) for user_model in users_model]
        return users_model
    except Exception as e:
        logger.error("Error getting all users")
        raise f"Error to get all users: {e}"

@router.delete("/delete/{user_id}")
def delete_user(user_id: str, user: UserModel = Depends(validate_api_key)):
    logger.info(f"Deleting user: {user_id}")
    try:
        return UsersAPIView().delete_user(user_id)
    except Exception as e:
        logger.error(f"Error deleting user: {user_id}")
        raise f"Error deleting user {user_id}: {e}"