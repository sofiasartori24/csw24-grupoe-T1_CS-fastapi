from sqlalchemy.orm import Session
from app.models.lesson import Lesson
from app.schemas.lesson import LessonCreate

class LessonRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Lesson).all()

    @staticmethod
    def get_by_id(db: Session, lesson_id: int):
        return db.query(Lesson).filter(Lesson.id == lesson_id).first()

    @staticmethod
    def create(db: Session, lesson: LessonCreate):
        db_lesson = Lesson(
            date=lesson.date,
            attendance=lesson.attendance,
            class_id=lesson.class_id,
            room_id=lesson.room_id,
            discipline_id=lesson.discipline_id,
        )
        db.add(db_lesson)
        db.commit()
        db.refresh(db_lesson)
        return db_lesson

    @staticmethod
    def delete(db: Session, lesson_id: int):
        db_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
        if db_lesson:
            db.delete(db_lesson)
            db.commit()
        return db_lesson