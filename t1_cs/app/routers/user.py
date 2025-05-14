from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.user import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/users", tags=["Users"])
        self.add_routes()

    def add_routes(self):
        @self.router.get("/", response_model=list[UserResponse])
        def get_users(db: Session = Depends(get_db)):
            service = UserService(db)
            return service.get_all_users()

        @self.router.get("/{user_id}", response_model=UserResponse)
        def get_user(user_id: int, db: Session = Depends(get_db)):
            service = UserService(db)
            return service.get_user_by_id(user_id)

        @self.router.post("/", response_model=UserResponse)
        def create_user(user: UserCreate, db: Session = Depends(get_db)):
            service = UserService(db)
            return service.create_user(user)

        @self.router.put("/{user_id}", response_model=UserResponse)
        def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
            service = UserService(db)
            return service.update_user(user_id, user_update)

        @self.router.delete("/{user_id}")
        def delete_user(user_id: int, db: Session = Depends(get_db)):
            service = UserService(db)
            service.delete_user(user_id)
            return {"message": "User deleted successfully"}
