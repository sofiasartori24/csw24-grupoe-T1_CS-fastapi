from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.profile import ProfileRepository
from app.schemas.profile import ProfileCreate

class ProfileService:
    def __init__(self):
        self.repository = ProfileRepository()
        
    def get_all_profiles(self, db: Session):
        return self.repository.get_all(db)

    def get_profile_by_id(self, db: Session, profile_id: int):
        profile = self.repository.get_by_id(db, profile_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return profile

    def create_profile(self, db: Session, profile: ProfileCreate):
        return self.repository.create(db, profile)

    def update_profile(self, db: Session, profile_id: int, profile: ProfileCreate):
        updated_profile = self.repository.update(db, profile_id, profile)
        if not updated_profile:
            raise HTTPException(status_code=404, detail="Profile not found for update")
        return updated_profile

    def delete_profile(self, db: Session, profile_id: int):
        success = self.repository.delete(db, profile_id)
        if not success:
            raise HTTPException(status_code=404, detail="Profile not found for deletion")
        return success
