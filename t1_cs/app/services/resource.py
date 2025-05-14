from sqlalchemy.orm import Session
from app.repositories.resource import ResourceRepository
from app.schemas.resource import ResourceCreate, ResourceUpdate
from fastapi import HTTPException

class ResourceService:
    def __init__(self, db: Session):
        self.repository = ResourceRepository(db)

    def get_all_resources(self):
        resources = self.repository.get_all()
        if not resources:
            raise HTTPException(status_code=404, detail="No resources found")
        return resources

    def get_resource_by_id(self, resource_id: int):
        resource = self.repository.get_by_id(resource_id)
        if not resource:
            raise HTTPException(status_code=404, detail="Resource not found")
        return resource

    def create_resource(self, resource_data: ResourceCreate):
        return self.repository.create(resource_data)

    def delete_resource(self, resource_id: int):
        resource = self.repository.delete(resource_id)
        if not resource:
            raise HTTPException(status_code=404, detail="Resource not found")
        return {"message": "Resource deleted successfully"}

    def update_resource(self, resource_id: int, resource_data: ResourceUpdate):
        resource = self.repository.update(resource_id, resource_data)
        if not resource:
            raise HTTPException(status_code=404, detail="Resource not found")
        return resource
