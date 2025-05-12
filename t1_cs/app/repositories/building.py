from sqlalchemy.orm import Session
from app.models.building import Building
from app.schemas.building import BuildingCreate

class BuildingRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Building).all()

    @staticmethod
    def get_by_id(db: Session, building_id: int):
        return db.query(Building).filter(Building.id == building_id).first()

    @staticmethod
    def create(db: Session, building: BuildingCreate):
        db_building = Building(**building.dict())
        db.add(db_building)
        db.commit()
        db.refresh(db_building)
        return db_building

    @staticmethod
    def delete(db: Session, building_id: int):
        db_building = db.query(Building).filter(Building.id == building_id).first()
        if db_building:
            db.delete(db_building)
            db.commit()
        return db_building