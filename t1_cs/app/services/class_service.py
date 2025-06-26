from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.class_repository import ClassRepository
from app.schemas.class_schema import ClassCreate, ClassUpdate

class ClassService:
    def __init__(self):
        self.repository = ClassRepository()

    def get_all_classes(self, db: Session):
        classes = self.repository.get_all(db)
        if not classes:
            raise HTTPException(status_code=404, detail="No classes found")
        return classes

    def get_class_by_id(self, db: Session, class_id: int):
        class_obj = self.repository.get_by_id(db, class_id)
        if not class_obj:
            raise HTTPException(status_code=404, detail="Class not found")
        return class_obj

    def create_class(self, db: Session, class_data: ClassCreate):
        return self.repository.create(db, class_data)

    def update_class(self, db: Session, class_id: int, class_update: ClassUpdate):
        class_obj = self.repository.update(db, class_id, class_update)
        if not class_obj:
            raise HTTPException(status_code=404, detail="Class not found")
        return class_obj

    def delete_class(self, class_id: int, user_id: int, db: Session):
       class_obj = self.repository.delete(db, class_id)
       if not class_obj:
           raise HTTPException(status_code=404, detail="Class not found")
       return {"message": "Class deleted successfully"}

