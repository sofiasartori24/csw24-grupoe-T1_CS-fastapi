from sqlalchemy.orm import Session
from app.repositories.room import RoomRepository
from app.schemas.room import RoomCreate

class RoomService:
    @staticmethod
    def get_all_rooms(db: Session):
        return RoomRepository.get_all(db)

    @staticmethod
    def get_room_by_id(db: Session, room_id: int):
        return RoomRepository.get_by_id(db, room_id)

    @staticmethod
    def create_room(db: Session, room: RoomCreate):
        return RoomRepository.create(db, room)

    @staticmethod
    def delete_room(db: Session, room_id: int):
        return RoomRepository.delete(db, room_id)