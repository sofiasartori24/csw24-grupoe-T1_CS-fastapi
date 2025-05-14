from sqlalchemy.orm import Session
from app.models.discipline import Discipline
from app.schemas.discipline import DisciplineCreate, DisciplineUpdate

class DisciplineRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Discipline).all()

    def get_by_id(self, discipline_id: int):
        return self.db.query(Discipline).filter(Discipline.id == discipline_id).first()

    def create(self, discipline: DisciplineCreate):
        db_discipline = Discipline(**discipline.dict())
        self.db.add(db_discipline)
        self.db.commit()
        self.db.refresh(db_discipline)
        return db_discipline

    def update(self, discipline_id: int, discipline_update: DisciplineUpdate):
        db_discipline = self.db.query(Discipline).filter(Discipline.id == discipline_id).first()
        if db_discipline:
            for key, value in discipline_update.dict(exclude_unset=True).items():
                setattr(db_discipline, key, value)
            self.db.commit()
            self.db.refresh(db_discipline)
        return db_discipline

    def delete(self, discipline_id: int):
        db_discipline = self.db.query(Discipline).filter(Discipline.id == discipline_id).first()
        if db_discipline:
            self.db.delete(db_discipline)
            self.db.commit()
        return db_discipline
