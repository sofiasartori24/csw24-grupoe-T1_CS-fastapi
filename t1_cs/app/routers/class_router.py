from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.class_service import ClassService
from app.schemas.class_schema import ClassCreate, ClassResponse
from app.dependencies.permissions import require_coordinator


router = APIRouter(prefix="/classes", tags=["Classes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[ClassResponse])
def get_classes(db: Session = Depends(get_db)):
    return ClassService.get_all_classes(db)

@router.post("/", response_model=ClassResponse, dependencies=[Depends(require_coordinator)])
def create_class(class_data: ClassCreate, db: Session = Depends(get_db)):
    return ClassService.create_class(db, class_data)
