from sqlalchemy.orm import Session
from app.models.building import Building
from app.schemas.building import BuildingCreate, BuildingUpdate

class BuildingRepository:
    def __init__(self):
        pass

    def get_all(self, db: Session):
        return db.query(Building).all()

    def get_by_id(self, db: Session, building_id: int):
        return db.query(Building).filter(Building.id == building_id).first()

    def create(self, db: Session, building: BuildingCreate):
        db_building = Building(**building.dict())
        db.add(db_building)
        db.commit()
        db.refresh(db_building)
        return db_building

    def update(self, db: Session, building_id: int, building_data: BuildingUpdate):
        db_building = self.get_by_id(db, building_id)
        if not db_building:
            return None

        for field, value in building_data.dict(exclude_unset=True).items():
            setattr(db_building, field, value)

        db.commit()
        db.refresh(db_building)
        db_building

    def delete(self, db: Session, building_id: int):
        db_building = self.get_by_id(db, building_id)
        if db_building:
            db.delete(db_building)
            db.commit()
        return db_building
