from sqlalchemy.orm import Session
from app.repositories.discipline import DisciplineRepository
from app.schemas.discipline import DisciplineCreate, DisciplineUpdate
from fastapi import HTTPException

class DisciplineService:
    def __init__(self):
        self.repository = DisciplineRepository()

    def get_all_disciplines(self, db: Session):
        disciplines = self.repository.get_all(db)
        if not disciplines:
            raise HTTPException(status_code=404, detail="No disciplines found")
        return disciplines

    def get_discipline_by_id(self, db: Session, discipline_id: int):
        discipline = self.repository.get_by_id(db, discipline_id)
        if not discipline:
            raise HTTPException(status_code=404, detail="Discipline not found")
        return discipline

    def create_discipline(self, db: Session, discipline: DisciplineCreate):
        return self.repository.create(db, discipline)

    def update_discipline(self, db: Session, discipline_id: int, discipline_update: DisciplineUpdate):
        discipline = self.repository.update(db, discipline_id, discipline_update)
        if not discipline:
            raise HTTPException(status_code=404, detail="Discipline not found")
        return discipline

    def delete_discipline(self, db: Session, discipline_id: int):
        discipline = self.repository.delete(db, discipline_id)
        if not discipline:
            raise HTTPException(status_code=404, detail="Discipline not found")
        return {"message": "Discipline deleted successfully"}
