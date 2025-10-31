from shutil import ExecError
from fastapi import APIRouter, HTTPException

from core.api.users import UsersAPIView
from database.models.users import UserModel
from models.users import UserBaseModel, UserUpdateModel, UserResponseModel

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/create")
def create_user(user: UserBaseModel):
    user_model = user.model_dump_json(exclude_unset=True)
    user_model = UserModel.model_validate_json(user_model)
    try:
        return UsersAPIView().create_user(user_model)
    except HTTPException as e:
        raise f"Error to create user: {e}"

@router.patch("/update/{user_id}")
def update_user(user_id: str, user: UserUpdateModel):
    user_model = user.model_dump_json(exclude_unset=True)
    user_model = UserModel.model_validate_json(user_model)
    try:
        return UsersAPIView().update_user(user_id, user_model)
    except HTTPException as e:
        raise f"Error to update user {user_id}: {e}"

@router.get("/get/{user_id}")
def get_user(user_id: str):
    try:
        user_model = UsersAPIView().get_user(user_id)
        user_model = UserResponseModel.model_validate_json(user_model.model_dump_json())
        return user_model
    except HTTPException as e:
        raise f"Error to get user {user_id}: {e}"

@router.get("/get-all")
def get_all_users():
    try:
        users_model = UsersAPIView().get_all_users()
        users_model = [UserResponseModel.model_validate_json(user_model.model_dump_json()) for user_model in users_model]
        return users_model
    except Exception as e:
        raise f"Error to get all users: {e}"

@router.delete("/delete/{user_id}")
def delete_user(user_id: str):
    try:
        return UsersAPIView().delete_user(user_id)
    except Exception as e:
        raise f"Error deleting user {user_id}: {e}"