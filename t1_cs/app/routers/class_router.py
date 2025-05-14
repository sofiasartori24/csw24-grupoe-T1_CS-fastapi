from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.class_service import ClassService
from app.schemas.class_schema import ClassCreate, ClassUpdate, ClassResponse
from app.dependencies.permissions import require_coordinator

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ClassRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/classes", tags=["Classes"])
        self.add_routes()

    def add_routes(self):
        @self.router.get("/", response_model=list[ClassResponse])
        def get_classes(db: Session = Depends(get_db)):
            service = ClassService(db)
            return service.get_all_classes()

        @self.router.get("/{class_id}", response_model=ClassResponse)
        def get_class_by_id(class_id: int, db: Session = Depends(get_db)):
            service = ClassService(db)
            return service.get_class_by_id(class_id)

        @self.router.post("/", response_model=ClassResponse, dependencies=[Depends(require_coordinator)])
        def create_class(class_data: ClassCreate, db: Session = Depends(get_db)):
            service = ClassService(db)
            return service.create_class(class_data)

        @self.router.put("/{class_id}", response_model=ClassResponse, dependencies=[Depends(require_coordinator)])
        def update_class(class_id: int, class_update: ClassUpdate, db: Session = Depends(get_db)):
            service = ClassService(db)
            return service.update_class(class_id, class_update)

        @self.router.delete("/{class_id}", dependencies=[Depends(require_coordinator)])
        def delete_class(class_id: int, db: Session = Depends(get_db)):
            service = ClassService(db)
            return service.delete_class(class_id)
