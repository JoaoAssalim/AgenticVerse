import uuid

from sqlmodel import Session, select
from fastapi import HTTPException

from database.config import engine
from database.models.users import UserModel
from core.auth.utils import hash_password

class UsersAPIView:
    def __init__(self):
        pass

    def create_user(self, user: UserModel):
        user.password = hash_password(user.password)
        with Session(engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        
    def get_user(self, user_id: str):
        with Session(engine) as session:
            user = session.get(UserModel, uuid.UUID(user_id))
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        
    def get_all_users(self):
        with Session(engine) as session:
            users = session.exec(select(UserModel)).all()
            return users
        
    def update_user(self, user_id: str, user: UserModel):
        if user.password:
            user.password = hash_password(user.password)

        with Session(engine) as session:
            user_db = session.get(UserModel, uuid.UUID(user_id))

            if not user_db:
                raise HTTPException(status_code=404, detail="User not found")
                
            user_data = user.model_dump(exclude_unset=True)
            user_db.sqlmodel_update(user_data)
            session.add(user_db)
            session.commit()
            session.refresh(user_db)
            return user_db
        
    def delete_user(self, user_id: str):
        with Session(engine) as session:
            session.delete(session.get(UserModel, uuid.UUID(user_id)))
            session.commit()