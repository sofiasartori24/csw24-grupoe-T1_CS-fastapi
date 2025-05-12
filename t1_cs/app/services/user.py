from sqlalchemy.orm import Session
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate

class UserService:
    @staticmethod
    def get_all_users(db: Session):
        return UserRepository.get_all(db)

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return UserRepository.get_by_id(db, user_id)

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        return UserRepository.create(db, user)

    @staticmethod
    def delete_user(db: Session, user_id: int):
        return UserRepository.delete(db, user_id)