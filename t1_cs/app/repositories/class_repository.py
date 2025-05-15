from sqlalchemy.orm import Session
from app.models.class_model import Class
from app.schemas.class_schema import ClassCreate, ClassUpdate

class ClassRepository:
    def __init__(self):
        pass

    def get_all(self, db: Session):
        return db.query(Class).all()

    def get_by_id(self, db: Session, class_id: int):
        return db.query(Class).filter(Class.id == class_id).first()

    def create(self, db: Session, class_data: ClassCreate):
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

    def update(self, db: Session, class_id: int, class_update: ClassUpdate):
        db_class = db.query(Class).filter(Class.id == class_id).first()
        if not db_class:
            return None
        update_data = class_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_class, key, value)
        db.commit()
        db.refresh(db_class)
        return db_class

    def delete(self, db: Session, class_id: int):
        db_class = db.query(Class).filter(Class.id == class_id).first()
        if db_class:
            db.delete(db_class)
            db.commit()
        return db_class
