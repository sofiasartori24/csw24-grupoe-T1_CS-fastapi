from sqlalchemy.orm import Session
from app.models.room import Room
from app.models.resource import Resource
from app.schemas.room import RoomCreate, RoomUpdate


class RoomRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Room).all()

    def get_by_id(self, room_id: int):
        return self.db.query(Room).filter(Room.id == room_id).first()

    def create(self, room: RoomCreate):
        db_room = Room(
            room_number=room.room_number,
            capacity=room.capacity,
            floor=room.floor,
            building_id=room.building_id,
        )
        
        if room.resource_ids:
            resources = self.db.query(Resource).filter(Resource.id.in_(room.resource_ids)).all()
            db_room.resources = resources

        self.db.add(db_room)
        self.db.commit()
        self.db.refresh(db_room)
        return db_room

    def update(self, room_id: int, room_update: RoomUpdate):
        db_room = self.get_by_id(room_id)
        if not db_room:
            return None

        if room_update.room_number is not None:
            db_room.room_number = room_update.room_number
        if room_update.capacity is not None:
            db_room.capacity = room_update.capacity
        if room_update.floor is not None:
            db_room.floor = room_update.floor
        if room_update.building_id is not None:
            db_room.building_id = room_update.building_id
        if room_update.resource_ids is not None:
            resources = self.db.query(Resource).filter(Resource.id.in_(room_update.resource_ids)).all()
            db_room.resources = resources

        self.db.commit()
        self.db.refresh(db_room)
        return db_room

    def delete(self, room_id: int):
        db_room = self.get_by_id(room_id)
        if db_room:
            self.db.delete(db_room)
            self.db.commit()
        return db_room
