from sqlalchemy.orm import Session
from app.models.room import Room
from app.models.resource import Resource
from app.schemas.room import RoomCreate

class RoomRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Room).all()

    @staticmethod
    def get_by_id(db: Session, room_id: int):
        return db.query(Room).filter(Room.id == room_id).first()

    @staticmethod
    def create(db: Session, room: RoomCreate):
        db_room = Room(
            room_number=room.room_number,
            capacity=room.capacity,
            floor=room.floor,
            building_id=room.building_id,
        )
        # Associate resources
        resources = db.query(Resource).filter(Resource.id.in_(room.resource_ids)).all()
        db_room.resources = resources

        db.add(db_room)
        db.commit()
        db.refresh(db_room)
        return db_room

    @staticmethod
    def delete(db: Session, room_id: int):
        db_room = db.query(Room).filter(Room.id == room_id).first()
        if db_room:
            db.delete(db_room)
            db.commit()
        return db_room