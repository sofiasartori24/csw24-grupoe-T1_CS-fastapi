from sqlalchemy.orm import Session
from app.repositories.curriculum import CurriculumRepository
from app.schemas.curriculum import CurriculumCreate

class CurriculumService:
    @staticmethod
    def get_all_curriculums(db: Session):
        return CurriculumRepository.get_all(db)

    @staticmethod
    def get_curriculum_by_id(db: Session, curriculum_id: int):
        return CurriculumRepository.get_by_id(db, curriculum_id)

    @staticmethod
    def create_curriculum(db: Session, curriculum: CurriculumCreate):
        return CurriculumRepository.create(db, curriculum)

    @staticmethod
    def delete_curriculum(db: Session, curriculum_id: int):
        return CurriculumRepository.delete(db, curriculum_id)