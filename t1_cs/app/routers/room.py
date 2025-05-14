from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.room import RoomService
from app.schemas.room import RoomCreate, RoomUpdate, RoomResponse

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

        @self.router.post("/", response_model=RoomResponse)
        def create_room(room: RoomCreate, db: Session = Depends(get_db)):
            service = RoomService(db)
            return service.create_room(room)

        @self.router.put("/{room_id}", response_model=RoomResponse)
        def update_room(room_id: int, room_update: RoomUpdate, db: Session = Depends(get_db)):
            service = RoomService(db)
            return service.update_room(room_id, room_update)

        @self.router.delete("/{room_id}")
        def delete_room(room_id: int, db: Session = Depends(get_db)):
            service = RoomService(db)
            return service.delete_room(room_id)
