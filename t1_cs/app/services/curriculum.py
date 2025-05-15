from sqlalchemy.orm import Session
from app.repositories.curriculum import CurriculumRepository
from app.schemas.curriculum import CurriculumCreate, CurriculumUpdate
from fastapi import HTTPException

class CurriculumService:
    def __init__(self):
        self.repository = CurriculumRepository()

    def get_all_curriculums(self, db: Session):
        return self.repository.get_all(db)

    def get_curriculum_by_id(self, db: Session, curriculum_id: int):
        curriculum = self.repository.get_by_id(db, curriculum_id)
        if not curriculum:
            raise HTTPException(status_code=404, detail="Curriculum not found")
        return curriculum

    def create_curriculum(self, db: Session, curriculum: CurriculumCreate):
        return self.repository.create(db, curriculum)

    def update_curriculum(self, db: Session, curriculum_id: int, curriculum_update: CurriculumUpdate):
        curriculum = self.repository.get_by_id(db, curriculum_id)
        if not curriculum:
            raise HTTPException(status_code=404, detail="Curriculum not found")
        
        updated_curriculum = self.repository.update(db, curriculum_id, curriculum_update)
        return updated_curriculum

    def delete_curriculum(self, db: Session, curriculum_id: int):
        curriculum = self.repository.delete(db, curriculum_id)
        if not curriculum:
            raise HTTPException(status_code=404, detail="Curriculum not found")
        return {"message": "Curriculum deleted successfully"}
