from http.client import HTTPException
from fastapi import APIRouter, Depends, Path
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
        self.service = UserService()
        self.add_routes()

    def add_routes(self):
        @self.router.get("/", response_model=list[UserResponse])
        def get_users(db: Session = Depends(get_db)):
            return self.service.get_all_users(db)

        @self.router.get("/{user_id}", response_model=UserResponse)
        def get_user(user_id: int, db: Session = Depends(get_db)):
            return self.service.get_user_by_id(db, user_id)

        @self.router.post("/{user_requesting_id}", response_model=UserResponse)
        def create_user(user_requesting_id: int, user: UserCreate, db: Session = Depends(get_db)):
            user_requesting = self.service.get_user_by_id(db, user_requesting_id)
            if not user_requesting:
                raise HTTPException(status_code=404, detail="User not found")
            require_admin(user_requesting)
            return self.service.create_user(db, user)

        @self.router.put("/{user_to_update_id}/{user_requesting_id}", response_model=UserResponse)
        def update_user(user_to_update_id: int, user_requesting_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
            user = self.service.get_user_by_id(db, user_requesting_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_admin(user)
            return self.service.update_user(db, user_to_update_id, user_update)

        @self.router.delete("/{user_to_delete_id}/{user_requesting_id}", status_code=204)
        def delete_user(
            user_to_delete_id: int = Path(...),
            user_requesting_id: int = Path(...),
            db: Session = Depends(get_db)
        ):
            user = self.service.get_user_by_id(db, user_requesting_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_admin(user)
            self.service.delete_user(db, user_to_delete_id)
            return {"message": "User deleted successfully"}
