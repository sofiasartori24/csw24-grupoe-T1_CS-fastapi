from sqlalchemy.orm import Session
from app.repositories.building import BuildingRepository
from app.schemas.building import BuildingCreate, BuildingUpdate

class BuildingService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = BuildingRepository(db)
    
    def get_all_buildings(self):
        return self.repository.get_all()

    def get_building_by_id(self, building_id: int):
        building = self.repository.get_by_id(building_id)
        if not building:
            raise ValueError(f"Building with id {building_id} not found")
        return building

    def create_building(self, building: BuildingCreate):
        return self.repository.create(building)

    def update_building(self, building_id: int, building_update: BuildingUpdate):
        existing_building = self.repository.get_by_id(building_id)
        if not existing_building:
            raise ValueError(f"Building with id {building_id} not found")
        
        return self.repository.update(building_id, building_update)

    def delete_building(self, building_id: int):
        existing_building = self.repository.get_by_id(building_id)
        if not existing_building:
            raise ValueError(f"Building with id {building_id} not found")
        
        return self.repository.delete(building_id)
