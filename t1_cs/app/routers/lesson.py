from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.lesson import LessonService
from app.schemas.lesson import LessonCreate, LessonResponse
from app.dependencies.permissions import require_professor


router = APIRouter(prefix="/lessons", tags=["Lessons"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[LessonResponse])
def get_lessons(db: Session = Depends(get_db)):
    return LessonService.get_all_lessons(db)

@router.get("/{lesson_id}", response_model=LessonResponse)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = LessonService.get_lesson_by_id(db, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

@router.post("/", response_model=LessonResponse, dependencies=[Depends(require_professor)])
def create_lesson(lesson: LessonCreate, db: Session = Depends(get_db)):
    return LessonService.create_lesson(db, lesson)

@router.delete("/{lesson_id}", dependencies=[Depends(require_professor)])
def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = LessonService.delete_lesson(db, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return {"message": "Lesson deleted successfully"}
