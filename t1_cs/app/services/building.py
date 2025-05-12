from sqlalchemy.orm import Session
from app.repositories.building import BuildingRepository
from app.schemas.building import BuildingCreate

class BuildingService:
    @staticmethod
    def get_all_buildings(db: Session):
        return BuildingRepository.get_all(db)

    @staticmethod
    def get_building_by_id(db: Session, building_id: int):
        return BuildingRepository.get_by_id(db, building_id)

    @staticmethod
    def create_building(db: Session, building: BuildingCreate):
        return BuildingRepository.create(db, building)

    @staticmethod
    def delete_building(db: Session, building_id: int):
        return BuildingRepository.delete(db, building_id)