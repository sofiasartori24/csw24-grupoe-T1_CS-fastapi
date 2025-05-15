from sqlalchemy.orm import Session
from app.models.discipline import Discipline
from app.schemas.discipline import DisciplineCreate, DisciplineUpdate

class DisciplineRepository:
    def __init__(self):
        pass

    def get_all(self, db: Session):
        return db.query(Discipline).all()

    def get_by_id(self, db: Session, discipline_id: int):
        return db.query(Discipline).filter(Discipline.id == discipline_id).first()

    def create(self, db: Session, discipline: DisciplineCreate):
        db_discipline = Discipline(**discipline.dict())
        db.add(db_discipline)
        db.commit()
        db.refresh(db_discipline)
        return db_discipline

    def update(self, db: Session, discipline_id: int, discipline_update: DisciplineUpdate):
        db_discipline = db.query(Discipline).filter(Discipline.id == discipline_id).first()
        if db_discipline:
            for key, value in discipline_update.dict(exclude_unset=True).items():
                setattr(db_discipline, key, value)
            db.commit()
            db.refresh(db_discipline)
        return db_discipline

    def delete(self, db: Session, discipline_id: int):
        db_discipline = db.query(Discipline).filter(Discipline.id == discipline_id).first()
        if db_discipline:
            db.delete(db_discipline)
            db.commit()
        return db_discipline
