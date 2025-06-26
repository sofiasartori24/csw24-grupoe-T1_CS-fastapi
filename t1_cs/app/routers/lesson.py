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
        self.service = LessonService()

    def add_routes(self):
        @self.router.get("/", response_model=list[LessonResponse])
        def get_lessons(db: Session = Depends(get_db)):
            return self.service.get_all_lessons(db)

        @self.router.get("/{lesson_id}", response_model=LessonResponse)
        def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
            return self.service.get_lesson_by_id(db, lesson_id)

        @self.router.post("/{user_id}", response_model=LessonResponse)
        def create_lesson(user_id: int, lesson: LessonCreate, db: Session = Depends(get_db)):
            user_service = UserService()
            user = user_service.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_professor(user)
            return self.service.create_lesson(db, lesson)
        
        @self.router.put("/{lesson_id}/{user_id}", response_model=LessonResponse)
        def update_lesson(lesson_id: int, user_id: int, lesson:LessonUpdate, db: Session = Depends(get_db)):
            user_service = UserService()
            user = user_service.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_professor(user)
            return self.service.update_lesson(db, lesson_id, lesson)

        @self.router.delete("/{lesson_id}/{user_id}")
        def delete_lesson(lesson_id: int, user_id: int, db: Session = Depends(get_db)):
            user_service = UserService()
            user = user_service.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_professor(user)
            return self.service.delete_lesson(db, lesson_id)
