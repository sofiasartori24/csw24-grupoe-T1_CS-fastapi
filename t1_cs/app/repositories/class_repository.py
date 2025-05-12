from sqlalchemy.orm import Session
from app.models.class_model import Class
from app.schemas.class_schema import ClassCreate

class ClassRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Class).all()

    @staticmethod
    def get_by_id(db: Session, class_id: int):
        return db.query(Class).filter(Class.id == class_id).first()

    @staticmethod
    def create(db: Session, class_data: ClassCreate):
        db_class = Class(
            semester=class_data.semester,
            schedule=class_data.schedule,
            vacancies=class_data.vacancies,
            discipline_id=class_data.discipline_id,
            professor_id=class_data.professor_id,
        )
        db.add(db_class)
        db.commit()
        db.refresh(db_class)
        return db_class

    @staticmethod
    def delete(db: Session, class_id: int):
        db_class = db.query(Class).filter(Class.id == class_id).first()
        if db_class:
            db.delete(db_class)
            db.commit()
        return db_class