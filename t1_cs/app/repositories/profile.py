from sqlalchemy.orm import Session
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate

class ProfileRepository:
    def __init__(self):
        pass

    def get_all(self, db: Session):
        return db.query(Profile).all()

    def get_by_id(self, db: Session, profile_id: int):
        return db.query(Profile).filter(Profile.id == profile_id).first()

    def create(self, db: Session, profile_data: ProfileCreate):
        db_profile = Profile(**profile_data.dict())
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile

    def update(self, db: Session, profile_id: int, profile_data: ProfileCreate):
        profile = self.get_by_id(db, profile_id)
        if not profile:
            return None
        for key, value in profile_data.dict(exclude_unset=True).items():
            setattr(profile, key, value)
        db.commit()
        db.refresh(profile)
        return profile

    def delete(self, db: Session, profile_id: int):
        profile = self.get_by_id(db, profile_id)
        if not profile:
            return False
        db.delete(profile)
        db.commit()
        return True
