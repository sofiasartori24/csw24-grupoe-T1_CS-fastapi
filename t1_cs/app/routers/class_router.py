from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.class_service import ClassService
from app.schemas.class_schema import ClassCreate, ClassUpdate, ClassResponse
from app.dependencies.permissions import require_coordinator
from app.services.user import UserService

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
        self.service = ClassService()

    def add_routes(self):
        @self.router.get("/", response_model=list[ClassResponse])
        def get_classes(db: Session = Depends(get_db)):
            return self.service.get_all_classes(db)

        @self.router.get("/{class_id}", response_model=ClassResponse)
        def get_class_by_id(class_id: int, db: Session = Depends(get_db)):
            return self.service.get_class_by_id(db, class_id)

        @self.router.post("/{user_id}", response_model=ClassResponse)
        def create_class(user_id: int, class_data: ClassCreate, db: Session = Depends(get_db)):
            user_service = UserService()
            user = user_service.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_coordinator(user)
            return self.service.create_class(db, class_data)

        @self.router.put("/{class_id}/{user_id}", response_model=ClassResponse, dependencies=[Depends(require_coordinator)])
        def update_class(class_id: int, user_id: int, class_update: ClassUpdate, db: Session = Depends(get_db)):
            user_service = UserService()
            user = user_service.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_coordinator(user)
            return self.service.update_class(db, class_id, class_update)

        @self.router.delete("/{class_id}/{user_id}", dependencies=[Depends(require_coordinator)])
        def delete_class(class_id: int, user_id: int, db: Session = Depends(get_db)):
            user_service = UserService()
            user = user_service.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_coordinator(user)
            return self.service.delete_class(db.class_id)
