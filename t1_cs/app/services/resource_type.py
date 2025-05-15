from sqlalchemy.orm import Session
from app.repositories.resource_type import ResourceTypeRepository
from app.schemas.resource_type import ResourceTypeCreate, ResourceTypeUpdate
from fastapi import HTTPException

class ResourceTypeService:
    def __init__(self):
        self.resource_type_repository = ResourceTypeRepository()

    def get_all_resource_types(self, db: Session):
        return self.resource_type_repository.get_all(db)

    def get_resource_type_by_id(self, db: Session, resource_type_id: int):
        resource_type = self.resource_type_repository.get_by_id(db, resource_type_id)
        if not resource_type:
            raise HTTPException(status_code=404, detail="ResourceType not found")
        return resource_type

    def create_resource_type(self, db: Session, resource_type: ResourceTypeCreate):
        return self.resource_type_repository.create(db, resource_type)

    def update_resource_type(self, db: Session, resource_type_id: int, resource_type_update: ResourceTypeUpdate):
        resource_type = self.resource_type_repository.update(db, resource_type_id, resource_type_update)
        if not resource_type:
            raise HTTPException(status_code=404, detail="ResourceType not found")
        return {"message": "ResourceType uptated successfully"}

    def delete_resource_type(self, db: Session, resource_type_id: int):
        resource_type = self.resource_type_repository.delete(db, resource_type_id)
        if not resource_type:
            raise HTTPException(status_code=404, detail="ResourceType not found")
        return {"message": "ResourceType deleted successfully"}
