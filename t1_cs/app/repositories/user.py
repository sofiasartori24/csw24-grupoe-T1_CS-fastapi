from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate

class UserRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(User).all()

    @staticmethod
    def get_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create(db: Session, user: UserCreate):
        # check if profile exists
        profile = db.query(User.profile.property.mapper.class_).get(user.profile_id)
        if not profile:
            raise ValueError(f"Profile with id {user.profile_id} does not exist")

        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def delete(db: Session, user_id: int):
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
        return db_user