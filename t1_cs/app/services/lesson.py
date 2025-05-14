from sqlalchemy.orm import Session
from app.repositories.lesson import LessonRepository
from app.schemas.lesson import LessonCreate, LessonUpdate
from fastapi import HTTPException

class LessonService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = LessonRepository(db)

    def get_all_lessons(self):
        lessons = self.repository.get_all()
        if not lessons:
            raise HTTPException(status_code=404, detail="No lessons found")
        return lessons

    def get_lesson_by_id(self, lesson_id: int):
        lesson = self.repository.get_by_id(lesson_id)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        return lesson

    def create_lesson(self, lesson_data: LessonCreate):
        return self.repository.create(lesson_data)

    def update_lesson(self, lesson_id: int, lesson_update: LessonUpdate):
        lesson = self.repository.update(lesson_id, lesson_update)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        return lesson

    def delete_lesson(self, lesson_id: int):
        lesson = self.repository.delete(lesson_id)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        return {"message": "Lesson deleted successfully"}
