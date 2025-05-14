from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.discipline import DisciplineService
from app.schemas.discipline import DisciplineCreate, DisciplineUpdate, DisciplineResponse

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DisciplineRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/disciplines", tags=["Disciplines"])
        self.add_routes()

    def add_routes(self):
        @self.router.get("/", response_model=list[DisciplineResponse])
        def get_disciplines(db: Session = Depends(get_db)):
            service = DisciplineService(db)
            return service.get_all_disciplines()

        @self.router.get("/{discipline_id}", response_model=DisciplineResponse)
        def get_discipline(discipline_id: int, db: Session = Depends(get_db)):
            service = DisciplineService(db)
            return service.get_discipline_by_id(discipline_id)

        @self.router.post("/", response_model=DisciplineResponse)
        def create_discipline(discipline: DisciplineCreate, db: Session = Depends(get_db)):
            service = DisciplineService(db)
            return service.create_discipline(discipline)

        @self.router.put("/{discipline_id}", response_model=DisciplineResponse)
        def update_discipline(discipline_id: int, discipline_update: DisciplineUpdate, db: Session = Depends(get_db)):
            service = DisciplineService(db)
            return service.update_discipline(discipline_id, discipline_update)

        @self.router.delete("/{discipline_id}")
        def delete_discipline(discipline_id: int, db: Session = Depends(get_db)):
            service = DisciplineService(db)
            return service.delete_discipline(discipline_id)
