from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.curriculum import CurriculumService
from app.schemas.curriculum import CurriculumCreate, CurriculumResponse, CurriculumUpdate
from app.dependencies.permissions import require_coordinator
from app.services.user import UserService


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CurriculumRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/curriculums", tags=["Curriculums"])
        self.add_routes()
        self.service = CurriculumService()

    def add_routes(self):
        @self.router.get("/", response_model=list[CurriculumResponse])
        def get_curriculums(db: Session = Depends(get_db)):
            return self.service.get_all_curriculums(db)

        @self.router.get("/{curriculum_id}", response_model=CurriculumResponse)
        def get_curriculum(curriculum_id: int, db: Session = Depends(get_db)):
            curriculum = self.service.get_curriculum_by_id(db, curriculum_id)
            return curriculum

        @self.router.post("/{user_id}", response_model=CurriculumResponse)
        def create_curriculum(user_id: int, curriculum: CurriculumCreate, db: Session = Depends(get_db)):
            user_service = UserService()
            user = user_service.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_coordinator(user)
            return self.service.create_curriculum(db, curriculum)

        @self.router.put("/{curriculum_id}/{user_id}", response_model=CurriculumResponse)
        def update_curriculum(user_id: int, curriculum_id: int, curriculum_update: CurriculumUpdate, db: Session = Depends(get_db)):
            user_service = UserService()
            user = user_service.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_coordinator(user)
            return self.service.update_curriculum(db, curriculum_id, curriculum_update)

        @self.router.delete("/{curriculum_id}/{user_id}")
        def delete_curriculum(user_id: int, curriculum_id: int, db: Session = Depends(get_db)):
            user_service = UserService()
            user = user_service.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_coordinator(user)
            return self.service.delete_curriculum(db, curriculum_id)
