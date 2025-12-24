import uuid
import logging

from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session, select

from database.config import engine
from core.auth.utils import hash_password
from database.models.users import UserModel

logger = logging.Logger(__name__)

class UsersAPIView:
    def __init__(self):
        pass

    def create_user(self, user: UserModel):
        logger.info("Creating user")

        if user.password and len(user.password) < 8:
            logger.error("Error to create user: Password is short")
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
        
        if not self.validate_email_exists(user.email):
            logger.error("Error to create user: Email already in use")
            raise HTTPException(status_code=409, detail="Email already in use")
        
        try:
            user.password = hash_password(user.password)
        
            with Session(engine) as session:
                session.add(user)
                session.commit()
                session.refresh(user)
                return user
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Error to create user: {e}")
            session.rollback()
            raise HTTPException(status_code=500, detail=e)
        
    def get_user(self, user_id: str):
        logger.info("Getting user")
        try:
            with Session(engine) as session:
                user = session.get(UserModel, uuid.UUID(user_id))
                if not user:
                    raise HTTPException(status_code=404, detail="User not found")
                return user
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Error to get user: {e}")
            session.rollback()
            raise HTTPException(status_code=500, detail=e)
    
    def validate_email_exists(self, email: str):
        logger.info(f"Validating user email: {email}")
        try:
            with Session(engine) as session:
                user = session.exec(select(UserModel).where(UserModel.email == email)).first()
                if user:
                    logger.error("User email already in use")
                    raise HTTPException(status_code=409, detail="Email already in use")
                return True
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Error to validate email: {e}")
            session.rollback()
            raise HTTPException(status_code=500, detail=e)
        
    def get_user_by_email(self, email: str):
        logger.info("Getting user by email")
        try:
            with Session(engine) as session:
                user = session.exec(select(UserModel).where(UserModel.email == email)).first()
                if not user:
                    logger.error("User not found")
                    raise HTTPException(status_code=404, detail="User not found")
                return user
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Error to get user by email: {e}")
            session.rollback()
            raise HTTPException(status_code=500, detail=e)
        
    def get_all_users(self):
        try:
            with Session(engine) as session:
                users = session.exec(select(UserModel)).all()
                return users
        except Exception as e:
            logger.error(f"Error to get all users: {e}")
            session.rollback()
            raise HTTPException(status_code=500, detail=e)
        
    def update_user(self, user_id: str, user: UserModel):
        logger.info(f"Updating user: {user_id}")
        try:
            if user.password:
                user.password = hash_password(user.password)
            
            if self.get_user_by_email(user.email) and self.get_user_by_email(user.email).id != user_id:
                logger.error("Error to update user: email already in use")
                raise HTTPException(status_code=409, detail="Email already in use")

            with Session(engine) as session:
                user_db = session.get(UserModel, uuid.UUID(user_id))

                if not user_db:
                    logger.error("Error to update user: user not found")
                    raise HTTPException(status_code=404, detail="User not found")
                    
                user_data = user.model_dump(exclude_unset=True)
                user_data["updated_at"] = datetime.now()
                user_db.sqlmodel_update(user_data)
                session.add(user_db)
                session.commit()
                session.refresh(user_db)
                return user_db
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Error to update user: {e}")
            session.rollback()
            raise HTTPException(status_code=500, detail=e)
        
    def delete_user(self, user_id: str):
        logger.info(f"Deleting user: {user_id}")
        try:
            with Session(engine) as session:
                session.delete(session.get(UserModel, uuid.UUID(user_id)))
                session.commit()
        except Exception as e:
            logger.error(f"Error to delete user: {e}")
            session.rollback()
            raise HTTPException(status_code=500, detail=e)