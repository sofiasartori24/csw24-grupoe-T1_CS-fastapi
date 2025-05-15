from sqlalchemy.orm import Session
from app.models.lesson import Lesson
from app.schemas.lesson import LessonCreate, LessonUpdate

class LessonRepository:
    def __init__(self):
        pass

    def get_all(self, db: Session):
        return db.query(Lesson).all()

    def get_by_id(self, db: Session, lesson_id: int):
        return db.query(Lesson).filter(Lesson.id == lesson_id).first()

    def create(self, db: Session, lesson: LessonCreate):
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

    def update(self, db: Session, lesson_id: int, lesson_update: LessonUpdate):
        db_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
        if db_lesson:
            for key, value in lesson_update.dict(exclude_unset=True).items():
                setattr(db_lesson, key, value)
            db.commit()
            db.refresh(db_lesson)
        return db_lesson 

    def delete(self, db: Session, lesson_id: int):
        db_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
        if db_lesson:
            db.delete(db_lesson)
            db.commit()
        return db_lesson 
