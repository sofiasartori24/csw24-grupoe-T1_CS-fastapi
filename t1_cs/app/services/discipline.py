from sqlalchemy.orm import Session
from app.repositories.discipline import DisciplineRepository
from app.schemas.discipline import DisciplineCreate

class DisciplineService:
    @staticmethod
    def get_all_disciplines(db: Session):
        return DisciplineRepository.get_all(db)

    @staticmethod
    def get_discipline_by_id(db: Session, discipline_id: int):
        return DisciplineRepository.get_by_id(db, discipline_id)

    @staticmethod
    def create_discipline(db: Session, discipline: DisciplineCreate):
        return DisciplineRepository.create(db, discipline)

    @staticmethod
    def delete_discipline(db: Session, discipline_id: int):
        return DisciplineRepository.delete(db, discipline_id)