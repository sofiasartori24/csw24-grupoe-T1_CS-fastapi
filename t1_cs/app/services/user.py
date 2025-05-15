from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_all_users(self, db: Session):
        return self.user_repository.get_all(db)

    def get_user_by_id(self, db: Session, user_id: int):
        user = self.user_repository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def create_user(self, db: Session, user: UserCreate):
        return self.user_repository.create(db, user)

    def update_user(self, db: Session, user_id: int, user_update: UserUpdate):
        existing_user = self.user_repository.get_by_id(db, user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        return self.user_repository.update(db, user_id, user_update)

    def delete_user(self, db: Session, user_id: int):
        existing_user = self.user_repository.get_by_id(db, user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        return self.user_repository.delete(db, user_id)
