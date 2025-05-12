from sqlalchemy.orm import Session
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate

class ProfileRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Profile).all()

    @staticmethod
    def get_by_id(db: Session, profile_id: int):
        return db.query(Profile).filter(Profile.id == profile_id).first()

    @staticmethod
    def create(db: Session, profile: ProfileCreate):
        db_profile = Profile(**profile.dict())
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile