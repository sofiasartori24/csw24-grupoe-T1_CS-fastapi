from sqlalchemy.orm import Session
from app.models.lesson import Lesson
from app.schemas.lesson import LessonCreate, LessonUpdate

class LessonRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Lesson).all()

    def get_by_id(self, lesson_id: int):
        return self.db.query(Lesson).filter(Lesson.id == lesson_id).first()

    def create(self, lesson: LessonCreate):
        db_lesson = Lesson(
            date=lesson.date,
            attendance=lesson.attendance,
            class_id=lesson.class_id,
            room_id=lesson.room_id,
            discipline_id=lesson.discipline_id,
        )
        self.db.add(db_lesson)
        self.db.commit()
        self.db.refresh(db_lesson)
        return db_lesson

    def update(self, lesson_id: int, lesson_update: LessonUpdate):
        db_lesson = self.db.query(Lesson).filter(Lesson.id == lesson_id).first()
        if db_lesson:
            for key, value in lesson_update.dict(exclude_unset=True).items():
                setattr(db_lesson, key, value)
            self.db.commit()
            self.db.refresh(db_lesson)
        return db_lesson 

    def delete(self, lesson_id: int):
        db_lesson = self.db.query(Lesson).filter(Lesson.id == lesson_id).first()
        if db_lesson:
            self.db.delete(db_lesson)
            self.db.commit()
        return db_lesson 
