from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.profile import ProfileService
from app.schemas.profile import ProfileCreate, ProfileResponse

router = APIRouter(prefix="/profiles", tags=["Profiles"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[ProfileResponse])
def get_profiles(db: Session = Depends(get_db)):
    return ProfileService.get_all_profiles(db)

@router.get("/{profile_id}", response_model=ProfileResponse)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = ProfileService.get_profile_by_id(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.post("/", response_model=ProfileResponse)
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    return ProfileService.create_profile(db, profile)