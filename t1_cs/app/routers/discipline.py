from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.discipline import DisciplineService
from app.schemas.discipline import DisciplineCreate, DisciplineUpdate, DisciplineResponse
from app.services.user import UserService
from app.dependencies.permissions import require_coordinator

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
        self.service = DisciplineService()

    def add_routes(self):
        @self.router.get("/", response_model=list[DisciplineResponse])
        def get_disciplines(db: Session = Depends(get_db)):
            return self.service.get_all_disciplines(db)

        @self.router.get("/{discipline_id}", response_model=DisciplineResponse)
        def get_discipline(discipline_id: int, db: Session = Depends(get_db)):
            return self.service.get_discipline_by_id(db, discipline_id)

        @self.router.post("/{user_id}", response_model=DisciplineResponse)
        def create_discipline(user_id: int, discipline: DisciplineCreate, db: Session = Depends(get_db)):
            user_service = UserService()
            user = user_service.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_coordinator(user)
            return self.service.create_discipline(db, discipline)

        @self.router.put("/{discipline_id}/{user_id}", response_model=DisciplineResponse)
        def update_discipline(discipline_id: int, user_id: int, discipline_update: DisciplineUpdate, db: Session = Depends(get_db)):
            user_service = UserService()
            user = user_service.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_coordinator(user)
            return self.service.update_discipline(db, discipline_id, discipline_update)

        @self.router.delete("/{discipline_id}/{user_id}")
        def delete_discipline(discipline_id: int, user_id:int, db: Session = Depends(get_db)):
            user_service = UserService()
            user = user_service.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_coordinator(user)
            return self.service.delete_discipline(db, discipline_id)
