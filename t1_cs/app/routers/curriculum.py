from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.curriculum import CurriculumService
from app.schemas.curriculum import CurriculumCreate, CurriculumResponse
from app.dependencies.permissions import require_coordinator


router = APIRouter(prefix="/curriculums", tags=["Curriculums"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[CurriculumResponse])
def get_curriculums(db: Session = Depends(get_db)):
    return CurriculumService.get_all_curriculums(db)

@router.get("/{curriculum_id}", response_model=CurriculumResponse)
def get_curriculum(curriculum_id: int, db: Session = Depends(get_db)):
    curriculum = CurriculumService.get_curriculum_by_id(db, curriculum_id)
    if not curriculum:
        raise HTTPException(status_code=404, detail="Curriculum not found")
    return curriculum

@router.post("/", response_model=CurriculumResponse, dependencies=[Depends(require_coordinator)])
def create_curriculum(curriculum: CurriculumCreate, db: Session = Depends(get_db)):
    return CurriculumService.create_curriculum(db, curriculum)

@router.delete("/{curriculum_id}", dependencies=[Depends(require_coordinator)])
def delete_curriculum(curriculum_id: int, db: Session = Depends(get_db)):
    curriculum = CurriculumService.delete_curriculum(db, curriculum_id)
    if not curriculum:
        raise HTTPException(status_code=404, detail="Curriculum not found")
    return {"message": "Curriculum deleted successfully"}
