from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.room import RoomRepository
from app.schemas.room import RoomCreate, RoomUpdate


class RoomService:
    def __init__(self):
        self.repository = RoomRepository()

    def get_all_rooms(self, db: Session):
        rooms = self.repository.get_all(db)
        if not rooms:
            raise HTTPException(status_code=404, detail="No rooms found")
        return rooms

    def get_room_by_id(self, db: Session, room_id: int):
        room = self.repository.get_by_id(db, room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        return room

    def create_room(self, db: Session, room: RoomCreate):
        return self.repository.create(db, room)

    def update_room(self, db: Session, room_id: int, room_update: RoomUpdate):
        updated_room = self.repository.update(db, room_id, room_update)
        if not updated_room:
            raise HTTPException(status_code=404, detail="Room not found")
        return updated_room

    def delete_room(self, db: Session, room_id: int):
        deleted_room = self.repository.delete(db, room_id)
        if not deleted_room:
            raise HTTPException(status_code=404, detail="Room not found")
        return {"message": "Room deleted successfully"}
