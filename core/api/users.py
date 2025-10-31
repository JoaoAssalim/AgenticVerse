import uuid
from datetime import datetime

from sqlmodel import Session, select
from fastapi import HTTPException

from database.config import engine
from database.models.users import UserModel
from core.auth.utils import hash_password

class UsersAPIView:
    def __init__(self):
        pass

    def create_user(self, user: UserModel):
        if user.password and len(user.password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
        
        if not self.validate_email_exists(user.email):
            raise HTTPException(status_code=409, detail="Email already in use")
        
        try:
            user.password = hash_password(user.password)
        
            with Session(engine) as session:
                session.add(user)
                session.commit()
                session.refresh(user)
                return user
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=e)
        
    def get_user(self, user_id: str):
        try:
            with Session(engine) as session:
                user = session.get(UserModel, uuid.UUID(user_id))
                if not user:
                    raise HTTPException(status_code=404, detail="User not found")
                return user
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=e)
    
    def validate_email_exists(self, email: str):
        try:
            with Session(engine) as session:
                user = session.exec(select(UserModel).where(UserModel.email == email)).first()
                if user:
                    raise HTTPException(status_code=409, detail="Email already in use")
                return True
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=e)
        
    def get_user_by_email(self, email: str):
        try:
            with Session(engine) as session:
                user = session.exec(select(UserModel).where(UserModel.email == email)).first()
                if not user:
                    raise HTTPException(status_code=404, detail="User not found")
                return user
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=e)
        
    def get_all_users(self):
        try:
            with Session(engine) as session:
                users = session.exec(select(UserModel)).all()
                return users
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=e)
        
    def update_user(self, user_id: str, user: UserModel):
        try:
            if user.password:
                user.password = hash_password(user.password)
            
            if self.get_user_by_email(user.email) and self.get_user_by_email(user.email).id != user_id:
                raise HTTPException(status_code=409, detail="Email already in use")

            with Session(engine) as session:
                user_db = session.get(UserModel, uuid.UUID(user_id))

                if not user_db:
                    raise HTTPException(status_code=404, detail="User not found")
                    
                user_data = user.model_dump(exclude_unset=True)
                user_data["updated_at"] = datetime.now()
                user_db.sqlmodel_update(user_data)
                session.add(user_db)
                session.commit()
                session.refresh(user_db)
                return user_db
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=e)
        
    def delete_user(self, user_id: str):
        try:
            with Session(engine) as session:
                session.delete(session.get(UserModel, uuid.UUID(user_id)))
                session.commit()
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=e)