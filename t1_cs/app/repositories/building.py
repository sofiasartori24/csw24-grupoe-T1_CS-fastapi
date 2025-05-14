from sqlalchemy.orm import Session
from app.models.building import Building
from app.schemas.building import BuildingCreate, BuildingUpdate

class BuildingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Building).all()

    def get_by_id(self, building_id: int):
        return self.db.query(Building).filter(Building.id == building_id).first()

    def create(self, building: BuildingCreate):
        db_building = Building(**building.dict())
        self.db.add(db_building)
        self.db.commit()
        self.db.refresh(db_building)
        return db_building

    def update(self, building_id: int, building_data: BuildingUpdate):
        db_building = self.get_by_id(building_id)
        if not db_building:
            return None

        for field, value in building_data.dict(exclude_unset=True).items():
            setattr(db_building, field, value)

        self.db.commit()
        self.db.refresh(db_building)
        return db_building

    def delete(self, building_id: int):
        db_building = self.get_by_id(building_id)
        if db_building:
            self.db.delete(db_building)
            self.db.commit()
        return db_building
