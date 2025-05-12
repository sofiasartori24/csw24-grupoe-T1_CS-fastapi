from sqlalchemy.orm import Session
from app.models.discipline import Discipline
from app.schemas.discipline import DisciplineCreate

class DisciplineRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Discipline).all()

    @staticmethod
    def get_by_id(db: Session, discipline_id: int):
        return db.query(Discipline).filter(Discipline.id == discipline_id).first()

    @staticmethod
    def create(db: Session, discipline: DisciplineCreate):
        db_discipline = Discipline(**discipline.dict())
        db.add(db_discipline)
        db.commit()
        db.refresh(db_discipline)
        return db_discipline

    @staticmethod
    def delete(db: Session, discipline_id: int):
        db_discipline = db.query(Discipline).filter(Discipline.id == discipline_id).first()
        if db_discipline:
            db.delete(db_discipline)
            db.commit()
        return db_discipline