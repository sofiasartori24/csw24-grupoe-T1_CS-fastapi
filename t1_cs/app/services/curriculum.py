from sqlalchemy.orm import Session
from app.repositories.curriculum import CurriculumRepository
from app.schemas.curriculum import CurriculumCreate, CurriculumUpdate
from fastapi import HTTPException

class CurriculumService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = CurriculumRepository(db)

    def get_all_curriculums(self):
        return self.repository.get_all()

    def get_curriculum_by_id(self, curriculum_id: int):
        curriculum = self.repository.get_by_id(curriculum_id)
        if not curriculum:
            raise HTTPException(status_code=404, detail="Curriculum not found")
        return curriculum

    def create_curriculum(self, curriculum: CurriculumCreate):
        return self.repository.create(curriculum)

    def update_curriculum(self, curriculum_id: int, curriculum_update: CurriculumUpdate):
        curriculum = self.repository.get_by_id(curriculum_id)
        if not curriculum:
            raise HTTPException(status_code=404, detail="Curriculum not found")
        
        updated_curriculum = self.repository.update(curriculum_id, curriculum_update)
        return updated_curriculum

    def delete_curriculum(self, curriculum_id: int):
        curriculum = self.repository.delete(curriculum_id)
        if not curriculum:
            raise HTTPException(status_code=404, detail="Curriculum not found")
        return {"message": "Curriculum deleted successfully"}
