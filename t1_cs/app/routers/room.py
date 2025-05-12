from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.room import RoomService
from app.schemas.room import RoomCreate, RoomResponse

router = APIRouter(prefix="/rooms", tags=["Rooms"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[RoomResponse])
def get_rooms(db: Session = Depends(get_db)):
    return RoomService.get_all_rooms(db)

@router.post("/", response_model=RoomResponse)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    return RoomService.create_room(db, room)