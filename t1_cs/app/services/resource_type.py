from sqlalchemy.orm import Session
from app.repositories.resource_type import ResourceTypeRepository
from app.schemas.resource_type import ResourceTypeCreate, ResourceTypeUpdate
from fastapi import HTTPException

class ResourceTypeService:
    def __init__(self, db: Session):
        self.db = db
        self.resource_type_repository = ResourceTypeRepository(db)

    def get_all_resource_types(self):
        return self.resource_type_repository.get_all()

    def get_resource_type_by_id(self, resource_type_id: int):
        resource_type = self.resource_type_repository.get_by_id(resource_type_id)
        if not resource_type:
            raise HTTPException(status_code=404, detail="ResourceType not found")
        return resource_type

    def create_resource_type(self, resource_type: ResourceTypeCreate):
        return self.resource_type_repository.create(resource_type)

    def update_resource_type(self, resource_type_id: int, resource_type_update: ResourceTypeUpdate):
        resource_type = self.resource_type_repository.update(resource_type_id, resource_type_update)
        if not resource_type:
            raise HTTPException(status_code=404, detail="ResourceType not found")
        return {"message": "ResourceType uptated successfully"}

    def delete_resource_type(self, resource_type_id: int):
        resource_type = self.resource_type_repository.delete(resource_type_id)
        if not resource_type:
            raise HTTPException(status_code=404, detail="ResourceType not found")
        return {"message": "ResourceType deleted successfully"}
