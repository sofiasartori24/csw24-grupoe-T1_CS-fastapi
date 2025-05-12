from sqlalchemy.orm import Session
from app.repositories.resource_type import ResourceTypeRepository
from app.schemas.resource_type import ResourceTypeCreate

class ResourceTypeService:
    @staticmethod
    def get_all_resource_types(db: Session):
        return ResourceTypeRepository.get_all(db)

    @staticmethod
    def get_resource_type_by_id(db: Session, resource_type_id: int):
        return ResourceTypeRepository.get_by_id(db, resource_type_id)

    @staticmethod
    def create_resource_type(db: Session, resource_type: ResourceTypeCreate):
        return ResourceTypeRepository.create(db, resource_type)

    @staticmethod
    def delete_resource_type(db: Session, resource_type_id: int):
        return ResourceTypeRepository.delete(db, resource_type_id)