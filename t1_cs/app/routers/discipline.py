from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.discipline import DisciplineService
from app.schemas.discipline import DisciplineCreate, DisciplineResponse

router = APIRouter(prefix="/disciplines", tags=["Disciplines"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[DisciplineResponse])
def get_disciplines(db: Session = Depends(get_db)):
    return DisciplineService.get_all_disciplines(db)

@router.get("/{discipline_id}", response_model=DisciplineResponse)
def get_discipline(discipline_id: int, db: Session = Depends(get_db)):
    discipline = DisciplineService.get_discipline_by_id(db, discipline_id)
    if not discipline:
        raise HTTPException(status_code=404, detail="Discipline not found")
    return discipline

@router.post("/", response_model=DisciplineResponse)
def create_discipline(discipline: DisciplineCreate, db: Session = Depends(get_db)):
    return DisciplineService.create_discipline(db, discipline)

@router.delete("/{discipline_id}")
def delete_discipline(discipline_id: int, db: Session = Depends(get_db)):
    discipline = DisciplineService.delete_discipline(db, discipline_id)
    if not discipline:
        raise HTTPException(status_code=404, detail="Discipline not found")
    return {"message": "Discipline deleted successfully"}