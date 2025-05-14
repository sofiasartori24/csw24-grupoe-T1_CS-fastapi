from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.curriculum import CurriculumService
from app.schemas.curriculum import CurriculumCreate, CurriculumResponse, CurriculumUpdate
from app.dependencies.permissions import require_coordinator


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

    def add_routes(self):
        @self.router.get("/", response_model=list[CurriculumResponse])
        def get_curriculums(db: Session = Depends(get_db)):
            service = CurriculumService(db)
            return service.get_all_curriculums()

        @self.router.get("/{curriculum_id}", response_model=CurriculumResponse)
        def get_curriculum(curriculum_id: int, db: Session = Depends(get_db)):
            service = CurriculumService(db)
            curriculum = service.get_curriculum_by_id(curriculum_id)
            if not curriculum:
                raise HTTPException(status_code=404, detail="Curriculum not found")
            return curriculum

        @self.router.post("/", response_model=CurriculumResponse, dependencies=[Depends(require_coordinator)])
        def create_curriculum(curriculum: CurriculumCreate, db: Session = Depends(get_db)):
            service = CurriculumService(db)
            return service.create_curriculum(curriculum)

        @self.router.put("/{curriculum_id}", response_model=CurriculumResponse, dependencies=[Depends(require_coordinator)])
        def update_curriculum(curriculum_id: int, curriculum_update: CurriculumUpdate, db: Session = Depends(get_db)):
            service = CurriculumService(db)
            curriculum = service.update_curriculum(curriculum_id, curriculum_update)
            if not curriculum:
                raise HTTPException(status_code=404, detail="Curriculum not found")
            return curriculum

        @self.router.delete("/{curriculum_id}", dependencies=[Depends(require_coordinator)])
        def delete_curriculum(curriculum_id: int, db: Session = Depends(get_db)):
            service = CurriculumService(db)
            curriculum = service.delete_curriculum(curriculum_id)
            if not curriculum:
                raise HTTPException(status_code=404, detail="Curriculum not found")
            return {"message": "Curriculum deleted successfully"}
