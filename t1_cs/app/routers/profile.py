from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.profile import ProfileService
from app.schemas.profile import ProfileCreate, ProfileResponse
from app.dependencies.permissions import require_admin
from app.services.user import UserService

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ProfileRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/profiles", tags=["Profiles"])
        self.add_routes()
        self.service = ProfileService()

    def add_routes(self):
        @self.router.get("/", response_model=list[ProfileResponse])
        def get_profiles(db: Session = Depends(get_db)):
            return self.service.get_all_profiles(db)

        @self.router.get("/{profile_id}", response_model=ProfileResponse)
        def get_profile(profile_id: int, db: Session = Depends(get_db)):
            return self.service.get_profile_by_id(db, profile_id)

        @self.router.post("/{user_id}", response_model=ProfileResponse)
        def create_profile(user_id: int, profile: ProfileCreate, db: Session = Depends(get_db)):
            user_service = UserService()
            user = user_service.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_admin(user)
            return self.service.create_profile(db, profile)

        @self.router.put("/{profile_id}/{user_id}", response_model=ProfileResponse)
        def update_profile(profile_id: int, user_id: int,  profile_update: ProfileCreate, db: Session = Depends(get_db)):
            user_service = UserService()
            user = user_service.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_admin(user)
            return self.service.update_profile(db, profile_id, profile_update)

        @self.router.delete("/{profile_id}/{user_id}", status_code=204)
        def delete_profile(profile_id: int, user_id: int, db: Session = Depends(get_db)):
            user_service = UserService()
            user = user_service.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_admin(user)
            return self.service.delete_profile(db, profile_id)
