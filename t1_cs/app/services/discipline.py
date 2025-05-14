from sqlalchemy.orm import Session
from app.repositories.discipline import DisciplineRepository
from app.schemas.discipline import DisciplineCreate, DisciplineUpdate
from fastapi import HTTPException

class DisciplineService:
    def __init__(self, db: Session):
        self.repository = DisciplineRepository(db)

    def get_all_disciplines(self):
        disciplines = self.repository.get_all()
        if not disciplines:
            raise HTTPException(status_code=404, detail="No disciplines found")
        return disciplines

    def get_discipline_by_id(self, discipline_id: int):
        discipline = self.repository.get_by_id(discipline_id)
        if not discipline:
            raise HTTPException(status_code=404, detail="Discipline not found")
        return discipline

    def create_discipline(self, discipline: DisciplineCreate):
        return self.repository.create(discipline)

    def update_discipline(self, discipline_id: int, discipline_update: DisciplineUpdate):
        discipline = self.repository.update(discipline_id, discipline_update)
        if not discipline:
            raise HTTPException(status_code=404, detail="Discipline not found")
        return discipline

    def delete_discipline(self, discipline_id: int):
        discipline = self.repository.delete(discipline_id)
        if not discipline:
            raise HTTPException(status_code=404, detail="Discipline not found")
        return {"message": "Discipline deleted successfully"}
