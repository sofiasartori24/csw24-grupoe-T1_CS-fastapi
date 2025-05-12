from sqlalchemy.orm import Session
from app.repositories.lesson import LessonRepository
from app.schemas.lesson import LessonCreate

class LessonService:
    @staticmethod
    def get_all_lessons(db: Session):
        return LessonRepository.get_all(db)

    @staticmethod
    def get_lesson_by_id(db: Session, lesson_id: int):
        return LessonRepository.get_by_id(db, lesson_id)

    @staticmethod
    def create_lesson(db: Session, lesson: LessonCreate):
        return LessonRepository.create(db, lesson)

    @staticmethod
    def delete_lesson(db: Session, lesson_id: int):
        return LessonRepository.delete(db, lesson_id)