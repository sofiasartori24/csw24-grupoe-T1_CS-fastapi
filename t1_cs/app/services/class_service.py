from sqlalchemy.orm import Session
from app.repositories.class_repository import ClassRepository
from app.schemas.class_schema import ClassCreate

class ClassService:
    @staticmethod
    def get_all_classes(db: Session):
        return ClassRepository.get_all(db)

    @staticmethod
    def get_class_by_id(db: Session, class_id: int):
        return ClassRepository.get_by_id(db, class_id)

    @staticmethod
    def create_class(db: Session, class_data: ClassCreate):
        return ClassRepository.create(db, class_data)

    @staticmethod
    def delete_class(db: Session, class_id: int):
        return ClassRepository.delete(db, class_id)