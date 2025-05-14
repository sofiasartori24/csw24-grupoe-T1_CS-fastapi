from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.room import RoomRepository
from app.schemas.room import RoomCreate, RoomUpdate


class RoomService:
    def __init__(self, db: Session):
        self.repository = RoomRepository(db)

    def get_all_rooms(self):
        rooms = self.repository.get_all()
        if not rooms:
            raise HTTPException(status_code=404, detail="No rooms found")
        return rooms

    def get_room_by_id(self, room_id: int):
        room = self.repository.get_by_id(room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        return room

    def create_room(self, room: RoomCreate):
        return self.repository.create(room)

    def update_room(self, room_id: int, room_update: RoomUpdate):
        updated_room = self.repository.update(room_id, room_update)
        if not updated_room:
            raise HTTPException(status_code=404, detail="Room not found")
        return updated_room

    def delete_room(self, room_id: int):
        deleted_room = self.repository.delete(room_id)
        if not deleted_room:
            raise HTTPException(status_code=404, detail="Room not found")
        return {"message": "Room deleted successfully"}
