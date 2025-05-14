from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.profile import ProfileService
from app.schemas.profile import ProfileCreate, ProfileResponse

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

    def add_routes(self):
        @self.router.get("/", response_model=list[ProfileResponse])
        def get_profiles(db: Session = Depends(get_db)):
            service = ProfileService(db)
            return service.get_all_profiles()

        @self.router.get("/{profile_id}", response_model=ProfileResponse)
        def get_profile(profile_id: int, db: Session = Depends(get_db)):
            service = ProfileService(db)
            return service.get_profile_by_id(profile_id)

        @self.router.post("/", response_model=ProfileResponse)
        def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
            service = ProfileService(db)
            return service.create_profile(profile)

        @self.router.put("/{profile_id}", response_model=ProfileResponse)
        def update_profile(profile_id: int, profile_update: ProfileCreate, db: Session = Depends(get_db)):
            service = ProfileService(db)
            return service.update_profile(profile_id, profile_update)

        @self.router.delete("/{profile_id}", status_code=204)
        def delete_profile(profile_id: int, db: Session = Depends(get_db)):
            service = ProfileService(db)
            return service.delete_profile(profile_id)
