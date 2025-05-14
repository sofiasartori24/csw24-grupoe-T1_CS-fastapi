from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.lesson import LessonService
from app.schemas.lesson import LessonCreate, LessonResponse, LessonUpdate
from app.dependencies.permissions import require_professor
from app.services.user import UserService

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class LessonRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/lessons", tags=["Lessons"])
        self.add_routes()

    def add_routes(self):
        @self.router.get("/", response_model=list[LessonResponse])
        def get_lessons(db: Session = Depends(get_db)):
            service = LessonService(db)
            return service.get_all_lessons()

        @self.router.get("/{lesson_id}", response_model=LessonResponse)
        def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
            service = LessonService(db)
            return service.get_lesson_by_id(lesson_id)

        @self.router.post("/{user_id}", response_model=LessonResponse)
        def create_lesson(user_id: int, lesson: LessonCreate, db: Session = Depends(get_db)):
            user_service = UserService(db)
            user = user_service.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_professor(user)
            service = LessonService(db)
            return service.create_lesson(lesson)
        
        @self.router.put("/{lesson_id}/{user_id}", response_model=LessonResponse)
        def update_lesson(user_id: int, lesson_id: int, lesson:LessonUpdate, db: Session = Depends(get_db)):
            user_service = UserService(db)
            user = user_service.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_professor(user)
            service = LessonService(db)
            return service.update_lesson(lesson_id, lesson)

        @self.router.delete("/{lesson_id}/{user_id}")
        def delete_lesson(user_id: int, lesson_id: int, db: Session = Depends(get_db)):
            user_service = UserService(db)
            user = user_service.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_professor(user)
            service = LessonService(db)
            return service.delete_lesson(lesson_id)
