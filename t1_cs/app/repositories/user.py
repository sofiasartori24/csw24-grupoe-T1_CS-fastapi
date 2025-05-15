from sqlalchemy.orm import Session
from app.models.user import User
from app.models.profile import Profile
from app.schemas.user import UserCreate, UserUpdate

class UserRepository:
    def __init__(self):
        pass

    def get_all(self, db: Session):
        return db.query(User).all()

    def get_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def create(self, db: Session, user: UserCreate):
        profile = db.query(Profile).get(user.profile_id)
        if not profile:
            raise ValueError(f"Profile with id {user.profile_id} does not exist")

        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update(self, db: Session, user_id: int, user_data: UserUpdate):
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None

        profile = db.query(Profile).get(user_data.profile_id)
        if not profile:
            raise ValueError(f"Profile with id {user_data.profile_id} does not exist")

        for key, value in user_data.dict().items():
            setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)
        return db_user

    def delete(self, db: Session, user_id: int):
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
        return db_user
