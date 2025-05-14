from http.client import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.user import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.dependencies.permissions import require_admin

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

        @self.router.post("/{user_to_create_id}/{user_requesting_id}", response_model=UserResponse)
        def create_user(user_to_create_id: int, user_requesting_id: int, user: UserCreate, db: Session = Depends(get_db)):
            service = UserService(db)
            user = service.get_user_by_id(user_requesting_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_admin(user)
            return service.create_user(user_to_create_id)

        @self.router.put("/{user_to_update_id}/{user_requesting_id}", response_model=UserResponse)
        def update_user(user_to_update_id: int, user_requesting_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
            service = UserService(db)
            user = service.get_user_by_id(user_requesting_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_admin(user)
            return service.update_user(user_to_update_id, user_update)

        @self.router.delete("/{user_to_delete_id}}/{user_requesting_id}")
        def delete_user(user_to_delete_id: int, user_requesting_id: int, db: Session = Depends(get_db)):
            service = UserService(db)
            user = service.get_user_by_id(user_requesting_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_admin(user)
            service.delete_user(user_to_delete_id)
            return {"message": "User deleted successfully"}
