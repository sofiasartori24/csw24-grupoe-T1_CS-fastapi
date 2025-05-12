from sqlalchemy.orm import Session
from app.repositories.profile import ProfileRepository
from app.schemas.profile import ProfileCreate

class ProfileService:
    @staticmethod
    def get_all_profiles(db: Session):
        return ProfileRepository.get_all(db)

    @staticmethod
    def get_profile_by_id(db: Session, profile_id: int):
        return ProfileRepository.get_by_id(db, profile_id)

    @staticmethod
    def create_profile(db: Session, profile: ProfileCreate):
        return ProfileRepository.create(db, profile)