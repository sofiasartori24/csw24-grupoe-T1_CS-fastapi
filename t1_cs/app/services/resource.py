from sqlalchemy.orm import Session
from app.repositories.resource import ResourceRepository
from app.schemas.resource import ResourceCreate
from app.schemas.resource import ResourceUpdate


class ResourceService:
    @staticmethod
    def get_all_resources(db: Session):
        return ResourceRepository.get_all(db)

    @staticmethod
    def get_resource_by_id(db: Session, resource_id: int):
        return ResourceRepository.get_by_id(db, resource_id)

    @staticmethod
    def create_resource(db: Session, resource: ResourceCreate):
        return ResourceRepository.create(db, resource)

    @staticmethod
    def delete_resource(db: Session, resource_id: int):
        return ResourceRepository.delete(db, resource_id)

    @staticmethod
    def update_resource(db: Session, resource_id: int, resource_data: ResourceUpdate):
        return ResourceRepository.update(db, resource_id, resource_data)