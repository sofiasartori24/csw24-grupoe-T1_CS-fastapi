from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.room import RoomService
from app.schemas.room import RoomCreate, RoomUpdate, RoomResponse
from app.dependencies.permissions import require_admin
from app.services.user import UserService

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class RoomRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/rooms", tags=["Rooms"])
        self.add_routes()

    def add_routes(self):
        @self.router.get("/", response_model=list[RoomResponse])
        def get_rooms(db: Session = Depends(get_db)):
            service = RoomService(db)
            return service.get_all_rooms()

        @self.router.get("/{room_id}", response_model=RoomResponse)
        def get_room_by_id(room_id: int, db: Session = Depends(get_db)):
            service = RoomService(db)
            return service.get_room_by_id(room_id)

        @self.router.post("/{user_id}", response_model=RoomResponse)
        def create_room(user_id: int, room: RoomCreate, db: Session = Depends(get_db)):
            user_service = UserService(db)
            user = user_service.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_admin(user)
            service = RoomService(db)
            return service.create_room(room)

        @self.router.put("/{room_id}/{user_id}", response_model=RoomResponse)
        def update_room(user_id: int, room_id: int, room_update: RoomUpdate, db: Session = Depends(get_db)):
            user_service = UserService(db)
            user = user_service.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_admin(user)
            service = RoomService(db)
            return service.update_room(room_id, room_update)

        @self.router.delete("/{room_id}/{user_id}")
        def delete_room(user_id: int, room_id: int, db: Session = Depends(get_db)):
            user_service = UserService(db)
            user = user_service.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_admin(user)
            service = RoomService(db)
            return service.delete_room(room_id)
