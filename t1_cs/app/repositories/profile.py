from sqlalchemy.orm import Session
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate

class ProfileRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Profile).all()

    def get_by_id(self, profile_id: int):
        return self.db.query(Profile).filter(Profile.id == profile_id).first()

    def create(self, profile_data: ProfileCreate):
        db_profile = Profile(**profile_data.dict())
        self.db.add(db_profile)
        self.db.commit()
        self.db.refresh(db_profile)
        return db_profile

    def update(self, profile_id: int, profile_data: ProfileCreate):
        profile = self.get_by_id(profile_id)
        if not profile:
            return None
        for key, value in profile_data.dict(exclude_unset=True).items():
            setattr(profile, key, value)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def delete(self, profile_id: int):
        profile = self.get_by_id(profile_id)
        if not profile:
            return False
        self.db.delete(profile)
        self.db.commit()
        return True
