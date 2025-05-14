from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.profile import ProfileRepository
from app.schemas.profile import ProfileCreate

class ProfileService:
    def __init__(self, db: Session):
        self.repository = ProfileRepository(db)
        
    def get_all_profiles(self):
        return self.repository.get_all()

    def get_profile_by_id(self, profile_id: int):
        profile = self.repository.get_by_id(profile_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return profile

    def create_profile(self, profile: ProfileCreate):
        return self.repository.create(profile)

    def update_profile(self, profile_id: int, profile: ProfileCreate):
        updated_profile = self.repository.update(profile_id, profile)
        if not updated_profile:
            raise HTTPException(status_code=404, detail="Profile not found for update")
        return updated_profile

    def delete_profile(self, profile_id: int):
        success = self.repository.delete(profile_id)
        if not success:
            raise HTTPException(status_code=404, detail="Profile not found for deletion")
        return success
