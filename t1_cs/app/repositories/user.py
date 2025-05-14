from sqlalchemy.orm import Session
from app.models.user import User
from app.models.profile import Profile
from app.schemas.user import UserCreate, UserUpdate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(User).all()

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def create(self, user: UserCreate):
        profile = self.db.query(Profile).get(user.profile_id)
        if not profile:
            raise ValueError(f"Profile with id {user.profile_id} does not exist")

        db_user = User(**user.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user_id: int, user_data: UserUpdate):
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None

        profile = self.db.query(Profile).get(user_data.profile_id)
        if not profile:
            raise ValueError(f"Profile with id {user_data.profile_id} does not exist")

        for key, value in user_data.dict().items():
            setattr(db_user, key, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete(self, user_id: int):
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
        return db_user
