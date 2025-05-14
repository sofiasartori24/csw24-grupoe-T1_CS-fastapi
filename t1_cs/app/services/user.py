from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def get_all_users(self):
        return self.user_repository.get_all()

    def get_user_by_id(self, user_id: int):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def create_user(self, user: UserCreate):
        return self.user_repository.create(user)

    def update_user(self, user_id: int, user_update: UserUpdate):
        existing_user = self.user_repository.get_by_id(user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        return self.user_repository.update(user_id, user_update)

    def delete_user(self, user_id: int):
        existing_user = self.user_repository.get_by_id(user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        return self.user_repository.delete(user_id)
