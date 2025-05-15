from sqlalchemy.orm import Session
from app.repositories.lesson import LessonRepository
from app.schemas.lesson import LessonCreate, LessonUpdate
from fastapi import HTTPException

class LessonService:
    def __init__(self):
        self.repository = LessonRepository()

    def get_all_lessons(self, db: Session):
        lessons = self.repository.get_all(db)
        if not lessons:
            raise HTTPException(status_code=404, detail="No lessons found")
        return lessons

    def get_lesson_by_id(self, db: Session, lesson_id: int):
        lesson = self.repository.get_by_id(db, lesson_id)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        return lesson

    def create_lesson(self, db: Session, lesson_data: LessonCreate):
        return self.repository.create(db, lesson_data)

    def update_lesson(self, db: Session, lesson_id: int, lesson_update: LessonUpdate):
        lesson = self.repository.update(db, lesson_id, lesson_update)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        return lesson

    def delete_lesson(self, db: Session, lesson_id: int):
        lesson = self.repository.delete(db, lesson_id)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        return {"message": "Lesson deleted successfully"}
