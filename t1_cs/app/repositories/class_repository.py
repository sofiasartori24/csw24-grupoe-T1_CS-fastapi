from sqlalchemy.orm import Session
from app.models.class_model import Class
from app.schemas.class_schema import ClassCreate, ClassUpdate

class ClassRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Class).all()

    def get_by_id(self, class_id: int):
        return self.db.query(Class).filter(Class.id == class_id).first()

    def create(self, class_data: ClassCreate):
        db_class = Class(
            semester=class_data.semester,
            schedule=class_data.schedule,
            vacancies=class_data.vacancies,
            discipline_id=class_data.discipline_id,
            professor_id=class_data.professor_id,
        )
        self.db.add(db_class)
        self.db.commit()
        self.db.refresh(db_class)
        return db_class

    def update(self, class_id: int, class_update: ClassUpdate):
        db_class = self.db.query(Class).filter(Class.id == class_id).first()
        if not db_class:
            return None
        update_data = class_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_class, key, value)
        self.db.commit()
        self.db.refresh(db_class)
        return db_class

    def delete(self, class_id: int):
        db_class = self.db.query(Class).filter(Class.id == class_id).first()
        if db_class:
            self.db.delete(db_class)
            self.db.commit()
        return db_class
