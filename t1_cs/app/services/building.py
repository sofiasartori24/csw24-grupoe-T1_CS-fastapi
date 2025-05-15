from sqlalchemy.orm import Session
from app.repositories.building import BuildingRepository
from app.schemas.building import BuildingCreate, BuildingUpdate

class BuildingService:
    def __init__(self):
        self.repository = BuildingRepository()
    
    def get_all_buildings(self, db: Session):
        return self.repository.get_all(db)

    def get_building_by_id(self, db: Session, building_id: int):
        building = self.repository.get_by_id(db, building_id)
        if not building:
            raise ValueError(f"Building with id {building_id} not found")
        return building

    def create_building(self, db: Session, building: BuildingCreate):
        return self.repository.create(db, building)

    def update_building(self, db: Session, building_id: int, building_update: BuildingUpdate):
        existing_building = self.repository.get_by_id(db, building_id)
        if not existing_building:
            raise ValueError(f"Building with id {building_id} not found")
        
        return self.repository.update(building_id, building_update)

    def delete_building(self, db: Session, building_id: int):
        existing_building = self.repository.get_by_id(db, building_id)
        if not existing_building:
            raise ValueError(f"Building with id {building_id} not found")
        
        return self.repository.delete(building_id)
